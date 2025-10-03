from injector import Injector, InstanceProvider
from taiwan_judicial_judgments_crawler.modules.crawling.exceptions.invalid_date import (
    InvalidDate,
)
from taiwan_judicial_judgments_crawler.modules.crawling.application.commands.collect_entries import (
    CollectEntries,
)
from taiwan_judicial_judgments_crawler.modules.crawling.domain.services.case_type_normalizer import (
    CaseTypeNormalizer,
)
from taiwan_judicial_judgments_crawler.modules.crawling.domain.services.court_name_normalizer import (
    CourtNameNormalizer,
)
from playwright.async_api import async_playwright, Page, BrowserContext
from taiwan_judicial_judgments_crawler.modules.general.enums.token import Token
from types import MethodType
from taiwan_judicial_judgments_crawler.modules.crawling.domain.services.case_number_extractor import (
    CaseNumberExtractor,
)
from taiwan_judicial_judgments_crawler.modules.crawling.application.commands.crawl import (
    Crawl,
)
from datetime import datetime, timedelta
from asyncio import Queue, create_task
from typing import Tuple


def validate(date_str: str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise InvalidDate()


def dates(start: datetime, end: datetime):
    current = start
    while current <= end:
        yield current.strftime("%Y-%m-%d")
        current += timedelta(days=1)


async def handle_scan(
    injector: Injector,
    case_type: str,
    court: str,
    start_date: str,
    end_date: str,
    /,
    take_screenshot: bool = False,
    save_html: bool = False,
    save_text: bool = False,
    save_json: bool = False,
):
    """
    爬取指定條件下的判決書，並解析詳情頁面儲存為 JSON。

    參數：
    - case_type: 案件類別，例如：民事、刑事、行政
    - court: 法院名稱，例如：台北地方法院（會自動正規化為：臺灣臺北地方法院）
    - date: 裁判日期（單日），格式 YYYY-MM-DD，例如：2025-09-01

    範例：
    python main.py crawl 民事 台北地方法院 2025-09-01
    python main.py crawl 刑事 臺灣高雄地方法院 2025-09-01
    """
    start = validate(start_date)
    end = validate(end_date)

    normalize_case_type = injector.get(CaseTypeNormalizer)
    normalize_court_name = injector.get(CourtNameNormalizer)
    extract_case_number = injector.get(CaseNumberExtractor)
    injector.binder.bind(Token.CaseType, normalize_case_type(case_type))
    injector.binder.bind(Token.Court, normalize_court_name(court))

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        injector.binder.bind(BrowserContext, InstanceProvider(context))
        page = await context.new_page()
        injector.binder.bind(Page, InstanceProvider(page))

        queue = Queue[Tuple[str, str]]()

        async def handle_crawl(injector: Injector, href: str):
            page = await context.new_page()
            injector.binder.bind(Page, InstanceProvider(page))
            try:
                await page.goto(href, wait_until="networkidle")
                handler = injector.get(Crawl)
                await handler(
                    take_screenshot=take_screenshot,
                    save_html=save_html,
                    save_text=save_text,
                    save_json=save_json,
                )
            finally:
                await page.close()

        async def worker():
            while True:
                title, href = await queue.get()
                try:
                    child_injector = injector.create_child_injector()
                    case_number = extract_case_number(title)
                    child_injector.binder.bind(
                        Token.CaseNumber, InstanceProvider(case_number)
                    )
                    handler = MethodType(handle_crawl, child_injector)
                    await handler(href)
                finally:
                    queue.task_done()

        tasks = [create_task(worker()) for _ in range(6)]

        try:
            for date_str in dates(start, end):
                injector.binder.bind(Token.DateStr, date_str)
                entries = injector.get(CollectEntries)
                async for title, href in entries():
                    await queue.put((title, href))
            await queue.join()
        finally:
            for task in tasks:
                task.cancel()
            await page.close()
            await context.close()
            await browser.close()
