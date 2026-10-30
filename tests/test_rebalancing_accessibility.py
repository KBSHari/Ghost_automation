import allure
import pytest
from playwright.sync_api import expect

from pages.rebalancing_page import RebalancingPage
from tests.allure_tags import rebalancing

MAX_TAB_PRESSES = 80


@pytest.mark.a11y
@rebalancing("Accessibility", "TC-067", "AC-013", "The model editor can be operated with the keyboard only")
def test_editor_reachable_by_keyboard(rebalancing_page: RebalancingPage):
    rebalancing_page.open()
    rebalancing_page.new_model_button.focus()
    rebalancing_page.page.keyboard.press("Enter")
    expect(rebalancing_page.editor.root).to_be_visible()

    editor = rebalancing_page.editor
    expect(editor.save_button).to_be_disabled()  # an empty model cannot be saved

    keyboard = rebalancing_page.page.keyboard
    with allure.step("Type a name and a valid model using the keyboard"):
        editor.name_input.focus()
        keyboard.type("Keyboard model")
        editor.asset_class_select.focus()
        keyboard.press("ArrowDown")  # first asset class in the list
        editor.root.locator("input[aria-label^='Target %']").first.focus()
        keyboard.type("100")
        expect(editor.save_button).to_be_enabled()

    with allure.step("Every control up to Save is reachable with Tab (no keyboard trap)"):
        editor.name_input.focus()
        reached = False
        for _ in range(MAX_TAB_PRESSES):
            keyboard.press("Tab")
            if editor.save_button.evaluate("el => el === document.activeElement"):
                reached = True
                break
        assert reached, "Save was not reachable with the Tab key"

    with allure.step("Pressing Enter on Save stores the model"):
        keyboard.press("Enter")
        expect(rebalancing_page.model_select).to_contain_text("Keyboard model")


@pytest.mark.a11y
@rebalancing("Accessibility", "TC-068", "AC-013", "Editor controls have accessible names")
def test_editor_controls_have_accessible_names(rebalancing_page: RebalancingPage):
    rebalancing_page.open()
    rebalancing_page.start_new_model()
    editor = rebalancing_page.editor
    editor.add_asset_class("EQUITY", "Equity", weight=100)

    expect(editor.name_input).to_be_visible()
    expect(editor.root.get_by_label("Name", exact=True)).to_be_visible()
    expect(editor.weight_input("Equity")).to_be_visible()
    expect(editor.min_input("Equity")).to_be_visible()
    expect(editor.max_input("Equity")).to_be_visible()
    expect(editor.root.get_by_role("button", name="Remove Equity")).to_be_visible()
