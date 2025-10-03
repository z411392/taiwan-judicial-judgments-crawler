from time import perf_counter
from injector import inject
from taiwan_judicial_judgments_crawler.modules.crawling.domain.ports.driven.judgement_repository import (
    JudgementRepository,
)
from playwright.async_api import Page
from logging import getLogger, Logger
from taiwan_judicial_judgments_crawler.modules.crawling.domain.services.output_path_calculator import (
    OutputPathCalculator,
)
from taiwan_judicial_judgments_crawler.modules.general.enums.token import Token
from taiwan_judicial_judgments_crawler.modules.crawling.domain.services.text_parser import (
    TextParser,
)
from bs4 import BeautifulSoup
from taiwan_judicial_judgments_crawler.modules.crawling.domain.services.json_parser import (
    JsonParser,
)


class Crawl:
    _judgement_repository: JudgementRepository
    _page: Page
    _logger: Logger
    _output_path_calculator: OutputPathCalculator
    _case_number: Token.CaseNumber
    _parse_text: TextParser
    _parse_json: JsonParser

    @inject
    def __init__(
        self,
        judgement_repository: JudgementRepository,
        page: Page,
        output_path_calculator: OutputPathCalculator,
        case_number: Token.CaseNumber,
        parse_text: TextParser,
        parse_json: JsonParser,
    ):
        self._judgement_repository = judgement_repository
        self._page = page
        self._logger = getLogger(__class__.__name__)
        self._output_path_calculator = output_path_calculator
        self._case_number = case_number
        self._parse_text = parse_text
        self._parse_json = parse_json

    async def _take_screenshot(self):
        screenshot_path = self._output_path_calculator(f"{self._case_number}.png")
        await self._page.screenshot(path=screenshot_path)

    async def _save_html(self, content: str):
        html_path = self._output_path_calculator(f"{self._case_number}.html")
        html = BeautifulSoup(content, "html.parser").prettify()
        await self._judgement_repository.save(
            html_path,
            html,
        )

    async def _save_text(self, text: str):
        text_path = self._output_path_calculator(f"{self._case_number}.txt")
        await self._judgement_repository.save(text_path, text)

    async def _save_json(self, json: str):
        json_path = self._output_path_calculator(f"{self._case_number}.json")
        await self._judgement_repository.save(json_path, json)

    async def __call__(
        self,
        /,
        take_screenshot: bool,
        save_html: bool,
        save_text: bool,
        save_json: bool,
    ):
        start = perf_counter()
        self._logger.info(f"crawling {self._page.url} started")
        try:
            content = ""
            if take_screenshot:
                await self._take_screenshot()
            if save_html or save_text or save_json:
                content = await self._page.content()
            if save_html:
                await self._save_html(content)
            if save_text or save_json:
                text = self._parse_text(content)
                if text:
                    if save_text:
                        await self._save_text(text)
                    if save_json:
                        json = await self._parse_json(text)
                        if json:
                            await self._save_json(json)
            elapsed = perf_counter() - start
            self._logger.info(f"crawling {self._page.url} finished in {elapsed:.2f}s")
        except Exception as exception:
            self._logger.exception(exception)
