import allure
from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class PortfolioPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.tabs = page.locator("gf-page-tabs")

    @allure.step("Open the Portfolio page")
    def open(self) -> "PortfolioPage":
        self.open_path("/portfolio")
        return self

    def tab(self, name: str) -> Locator:
        return self.tabs.get_by_role("tab", name=name, exact=True)

    @property
    def rebalancing_tab(self) -> Locator:
        return self.tab("Rebalancing")

    @allure.step("Click the Rebalancing tab")
    def open_rebalancing_tab(self) -> None:
        self.rebalancing_tab.click()
