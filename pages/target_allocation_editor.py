import re

import allure
from playwright.sync_api import Locator, Page


class TargetAllocationEditor:
    """The model editor shown after New model / Edit (gf-target-allocation-editor)."""

    def __init__(self, page: Page):
        self.root = page.locator("gf-target-allocation-editor")
        self.name_input = self.root.locator("#target-allocation-name")
        self.asset_class_select = self.root.locator("#add-asset-class")
        self.errors = self.root.locator(".alert-danger")
        self.save_button = self.root.get_by_role("button", name="Save", exact=True)
        self.cancel_button = self.root.get_by_role("button", name="Cancel", exact=True)
        self.flat_fee_input = self.root.locator("#param-flat-fee")
        self.allow_sells_checkbox = self.root.locator("#param-allow-sells")

    def weight_input(self, level_label: str) -> Locator:
        return self.root.get_by_label(re.compile(rf"^Target % {re.escape(level_label)}$"))

    def min_input(self, level_label: str) -> Locator:
        return self.root.get_by_label(re.compile(rf"^Minimum % {re.escape(level_label)}$"))

    def max_input(self, level_label: str) -> Locator:
        return self.root.get_by_label(re.compile(rf"^Maximum % {re.escape(level_label)}$"))

    @allure.step("Enter the model name: {name}")
    def set_name(self, name: str) -> None:
        self.name_input.fill(name)

    @allure.step("Add asset class {asset_class} with a target of {weight}%")
    def add_asset_class(self, asset_class: str, label: str, weight: float) -> None:
        self.asset_class_select.select_option(value=asset_class)
        self.weight_input(label).fill(str(weight))

    @allure.step("Set the target of {label} to {weight}%")
    def set_weight(self, label: str, weight: float) -> None:
        self.weight_input(label).fill(str(weight))

    @allure.step("Save the model")
    def save(self) -> None:
        self.save_button.click()
