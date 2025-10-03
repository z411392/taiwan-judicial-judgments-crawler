from playwright.async_api import Page
from injector import inject
from urllib.parse import urljoin


class EntriesCollector:
    _page: Page

    @inject
    def __init__(
        self,
        page: Page,
    ):
        self._page = page

    async def __call__(self):
        iframe = self._page.frame_locator("iframe").first
        body = iframe.locator("body")
        await body.wait_for(state="visible")
        table = iframe.locator("table").first
        await table.wait_for(state="visible")
        links = table.locator('a[href*="data.aspx"]')
        link_count = await links.count()
        if link_count == 0:
            return
        for index in range(link_count):
            link = links.nth(index)
            title = (await link.inner_text()).strip()
            href = urljoin(
                "https://judgment.judicial.gov.tw/FJUD/",
                await link.get_attribute("href"),
            )
            yield title, href
