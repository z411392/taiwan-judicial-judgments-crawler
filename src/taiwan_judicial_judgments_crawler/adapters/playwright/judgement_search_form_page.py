from playwright.async_api import Page
from injector import inject


class JudgementSearchFormPage:
    _page: Page

    @inject
    def __init__(self, page: Page):
        self._page = page

    async def _select_court(self, court_code: str):
        await self._page.select_option("#jud_court", court_code)

    async def _select_case_type(self, case_type: str):
        if case_type == "民事":
            return
        checkbox = self._page.get_by_role("checkbox", name=case_type)
        await checkbox.check()

    async def _fill_start_date(
        self,
        minguo_year: int,
        minguo_month: int,
        minguo_day: int,
    ):
        start_year_input, start_month_input, start_day_input = (
            self._page.get_by_title("開始日期的年度"),
            self._page.get_by_title("開始日期的月份"),
            self._page.get_by_title("開始日期的日"),
        )
        await start_year_input.fill(str(minguo_year))
        await start_month_input.fill(str(minguo_month))
        await start_day_input.fill(str(minguo_day))

    async def _fill_end_date(
        self,
        minguo_year: int,
        minguo_month: int,
        minguo_day: int,
    ):
        end_year_input, end_month_input, end_day_input = (
            self._page.get_by_title("結束日期的年度"),
            self._page.get_by_title("結束日期的月份"),
            self._page.get_by_title("結束日期的日"),
        )
        await end_year_input.fill(str(minguo_year))
        await end_month_input.fill(str(minguo_month))
        await end_day_input.fill(str(minguo_day))

    async def apply_fillters(
        self,
        court_code: str,
        case_type: str,
        minguo_year: int,
        minguo_month: int,
        minguo_day: int,
    ):
        await self._select_court(court_code)
        await self._select_case_type(case_type)
        await self._fill_start_date(
            minguo_year,
            minguo_month,
            minguo_day,
        )
        await self._fill_end_date(
            minguo_year,
            minguo_month,
            minguo_day,
        )

    async def submit(self):
        submit_button = self._page.get_by_role("button", name="送出查詢")
        await submit_button.click()
        await self._page.wait_for_load_state("networkidle")
