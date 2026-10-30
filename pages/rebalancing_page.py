import re

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.rebalancing_result import RebalancingResult
from pages.target_allocation_editor import TargetAllocationEditor


class RebalancingPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="Rebalancing", exact=True)
        self.error_alert = page.locator(".container > .alert-danger")
        self.new_model_button = page.get_by_role("button", name="New model")
        self.model_select = page.locator("#rebalancing-model")
        self.edit_button = page.get_by_role("button", name="Edit", exact=True)
        self.delete_button = page.get_by_role("button", name="Delete", exact=True)
        self.calculate_button = page.get_by_role("button", name="Calculate trades")
        self.allow_sells_checkbox = page.locator("#rebalancing-allow-sells")
        self.empty_state = page.get_by_text("You have no target model yet")
        self.editor = TargetAllocationEditor(page)
        self.result = RebalancingResult(page)

    @allure.step("Open the Rebalancing page")
    def open(self) -> "RebalancingPage":
        self.open_path("/portfolio/rebalancing")
        return self

    @allure.step("Click New model")
    def start_new_model(self) -> None:
        self.new_model_button.click()

    @allure.step("Click Edit")
    def start_edit(self) -> None:
        self.edit_button.click()

    @allure.step("Delete the selected model and confirm")
    def delete_selected_model(self) -> None:
        self.delete_button.click()
        dialog = self.page.get_by_role("dialog")
        dialog.get_by_role("button", name=re.compile(r"^(Yes|OK|Confirm|Delete)$")).click()

    @allure.step("Calculate trades")
    def calculate(self) -> None:
        self.calculate_button.click()

    def model_names(self) -> list[str]:
        return [text.strip() for text in self.model_select.locator("option").all_inner_texts()]
