from injector import Module, Binder, ClassProvider, Provider, Injector
from taiwan_judicial_judgments_crawler.modules.crawling.domain.ports.driven.judgement_repository import (
    JudgementRepository,
)
from taiwan_judicial_judgments_crawler.adapters.file_system.judgement_file_system_adapter import (
    JudgementFileSystemAdapter,
)
from langchain.schema import SystemMessage
from langchain_ollama import ChatOllama
from taiwan_judicial_judgments_crawler.modules.crawling.domain.services.json_parser import (
    JsonParser,
)


class JsonParserProvider(Provider[JsonParser]):
    def get(self, injector: Injector):
        prompt = ""
        with open("prompt.md", "r", encoding="utf-8") as handle:
            prompt = handle.read()
        llm = injector.get(ChatOllama)
        system_message = SystemMessage(content=prompt)
        return JsonParser(llm, system_message)


class CrawlingModule(Module):
    def configure(self, binder: Binder):
        binder.bind(JudgementRepository, ClassProvider(JudgementFileSystemAdapter))
        binder.bind(JsonParser, JsonParserProvider())


crawling_module = CrawlingModule()
