from injector import inject
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from logging import getLogger, Logger, LoggerAdapter
from re import search
from json import loads, dumps
from json_repair import repair_json


class InvalidJson(Exception):
    pass


class JsonParser:
    _llm: ChatOpenAI
    _prompt: str
    _system_message: SystemMessage
    _logger: Logger

    @inject
    def __init__(
        self,
        llm: ChatOpenAI,
        system_message: SystemMessage,
    ):
        self._llm = llm
        self._system_message = system_message
        self._logger = getLogger(__class__.__name__)

    def _remove_comments(self, obj):
        if isinstance(obj, dict):
            keys_to_remove = [k for k in obj if str(k).startswith("_comment")]
            for k in keys_to_remove:
                obj.pop(k)
            for k, v in obj.items():
                obj[k] = self._remove_comments(v)
        elif isinstance(obj, list):
            obj = [self._remove_comments(item) for item in obj]
        return obj

    def _extract_json_block(self, text: str):
        markdown_match = search(r"```json\s*([\s\S]*?)\s*```", text)
        json_text = ""
        if markdown_match:
            json_text = markdown_match.group(1).strip()
        else:
            first_brace = text.find("{")
            last_brace = text.rfind("}")

            if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
                json_text = text[first_brace : last_brace + 1]

        if not json_text:
            raise InvalidJson()

        try:
            repaired = repair_json(json_text)
            obj: dict = loads(repaired)
            return dumps(self._remove_comments(obj), indent=2, ensure_ascii=False)
        except Exception:
            raise InvalidJson()

    async def __call__(self, text: str):
        prompt = f"""以下為要處理的文本
---
{text}"""
        user_message = HumanMessage(content=prompt)
        LoggerAdapter(self._logger, dict(stage="request")).debug(text)
        response = await self._llm.agenerate([[self._system_message, user_message]])
        response_text = response.generations[0][0].text.strip()
        LoggerAdapter(self._logger, dict(stage="response")).debug(response_text)
        json = self._extract_json_block(response_text)
        self._logger.debug(json)
        return json
