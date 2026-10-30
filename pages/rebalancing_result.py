import allure
from playwright.sync_api import Download, Page


class RebalancingResult:
    """The result section shown after Calculate trades (gf-rebalancing-result)."""

    def __init__(self, page: Page):
        self.page = page
        self.root = page.locator("gf-rebalancing-result")
        self.heading = self.root.get_by_role("heading", name="Recommended trades")
        self.message = self.root.locator(".alert-info")
        self.trade_rows = self.root.locator("table").first.locator("tbody tr")
        self.export_json_button = self.root.get_by_role("button", name="Export JSON")
        self.export_csv_button = self.root.get_by_role("button", name="Export CSV")
        self.summary = self.root.locator("dl")

    @allure.step("Download the CSV export")
    def download_csv(self) -> Download:
        with self.page.expect_download() as download_info:
            self.export_csv_button.click()
        return download_info.value

    @allure.step("Download the JSON export")
    def download_json(self) -> Download:
        with self.page.expect_download() as download_info:
            self.export_json_button.click()
        return download_info.value
