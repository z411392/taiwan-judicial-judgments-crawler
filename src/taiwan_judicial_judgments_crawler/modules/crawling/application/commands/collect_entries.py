from injector import inject
from logging import getLogger, Logger
from time import perf_counter

from taiwan_judicial_judgments_crawler.modules.crawling.domain.services.minguo_date_transformer import (
    MinguoDateTransformer,
)
from playwright.async_api import Page
from taiwan_judicial_judgments_crawler.adapters.playwright.judgement_search_form_page import (
    JudgementSearchFormPage,
)
from taiwan_judicial_judgments_crawler.modules.crawling.domain.services.court_code_transformer import (
    CourtCodeTransformer,
)

from playwright.async_api import BrowserContext
from taiwan_judicial_judgments_crawler.modules.general.enums.token import Token
from taiwan_judicial_judgments_crawler.modules.crawling.domain.services.entries_collector import (
    EntriesCollector,
)


class CollectEntries:
    _page: Page
    _search_from_page: JudgementSearchFormPage
    _to_minguo: MinguoDateTransformer
    _to_court_code: CourtCodeTransformer
    _context: BrowserContext
    _case_type: Token.CaseType
    _court: Token.Court
    _date_str: Token.DateStr
    _collect_entries: EntriesCollector
    _logger: Logger

    @inject
    def __init__(
        self,
        page: Page,
        judgement_search_form_page: JudgementSearchFormPage,
        to_minguo: MinguoDateTransformer,
        to_court_code: CourtCodeTransformer,
        context: BrowserContext,
        case_type: Token.CaseType,
        court: Token.Court,
        date_str: Token.DateStr,
        collect_entries: EntriesCollector,
    ):
        self._page = page
        self._search_from_page = judgement_search_form_page
        self._to_minguo = to_minguo
        self._to_court_code = to_court_code
        self._context = context
        self._case_type = case_type
        self._court = court
        self._date_str = date_str
        self._collect_entries = collect_entries
        self._logger = getLogger(__class__.__name__)

    async def _search(
        self,
    ):
        await self._page.goto(
            "https://judgment.judicial.gov.tw/FJUD/Default_AD.aspx",
            wait_until="domcontentloaded",
        )
        court_code = self._to_court_code(self._court)
        minguo_year, minguo_month, minguo_day = self._to_minguo(self._date_str)
        await self._search_from_page.apply_fillters(
            court_code,
            self._case_type,
            minguo_year,
            minguo_month,
            minguo_day,
        )
        await self._search_from_page.submit()

    async def __call__(self):
        start = perf_counter()
        self._logger.info(f"{self._case_type}/{self._court}/{self._date_str} started")
        try:
            await self._search()
            async for title, href in self._collect_entries():
                yield title, href

            elapsed = perf_counter() - start
            self._logger.info(
                f"{self._case_type}/{self._court}/{self._date_str} finished in {elapsed:.2f}s"
            )
        except Exception as exception:
            self._logger.exception(exception)
