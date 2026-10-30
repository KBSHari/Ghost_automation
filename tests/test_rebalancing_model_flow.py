import allure
import pytest
from playwright.sync_api import expect

from pages.rebalancing_page import RebalancingPage
from tests.allure_tags import rebalancing
from utils.api_client import ApiClient

CRITICAL = allure.severity_level.CRITICAL

EQUITY = ("EQUITY", "Equity")
FIXED_INCOME = ("FIXED_INCOME", "Fixed Income")


def build_valid_model(editor, name: str) -> None:
    editor.set_name(name)
    editor.add_asset_class(*EQUITY, weight=60)
    editor.add_asset_class(*FIXED_INCOME, weight=40)


@pytest.mark.regression
@rebalancing("Model management", "TC-050", "AC-009a", "Create a model, run it and see the result", CRITICAL)
def test_full_flow_create_model_and_run(rebalancing_page: RebalancingPage):
    rebalancing_page.open()
    expect(rebalancing_page.empty_state).to_be_visible()

    rebalancing_page.start_new_model()
    build_valid_model(rebalancing_page.editor, "Growth 60/40")
    expect(rebalancing_page.editor.errors).to_have_count(0)
    rebalancing_page.editor.save()

    expect(rebalancing_page.editor.root).to_have_count(0)
    expect(rebalancing_page.model_select).to_contain_text("Growth 60/40")

    rebalancing_page.calculate()
    expect(rebalancing_page.result.heading).to_be_visible()
    # A brand-new user has no holdings: the planner explains instead of failing
    expect(rebalancing_page.result.message).to_be_visible()
    expect(rebalancing_page.error_alert).to_have_count(0)


@rebalancing("Model management", "TC-051", "AC-009a", "Edit and delete a model")
def test_edit_then_delete_model(rebalancing_page: RebalancingPage, api: ApiClient, user_with_flag):
    api.create_model(
        user_with_flag.auth_token,
        "Before edit",
        [{"assetClass": "EQUITY", "weight": 60}, {"assetClass": "FIXED_INCOME", "weight": 40}],
    )
    rebalancing_page.open()
    expect(rebalancing_page.model_select).to_contain_text("Before edit")

    rebalancing_page.start_edit()
    rebalancing_page.editor.set_name("After edit")
    rebalancing_page.editor.save()
    expect(rebalancing_page.model_select).to_contain_text("After edit")
    expect(rebalancing_page.model_select).not_to_contain_text("Before edit")

    rebalancing_page.delete_selected_model()
    expect(rebalancing_page.empty_state).to_be_visible()


@rebalancing("Validation", "TC-052", "AC-009b", "Inline error when the targets do not sum to 100%", CRITICAL)
def test_inline_error_when_targets_sum_to_99(rebalancing_page: RebalancingPage):
    rebalancing_page.open()
    rebalancing_page.start_new_model()
    editor = rebalancing_page.editor
    editor.set_name("Invalid 99")
    editor.add_asset_class(*EQUITY, weight=60)
    editor.add_asset_class(*FIXED_INCOME, weight=39)

    expect(editor.errors).to_be_visible()
    expect(editor.errors).to_contain_text("must sum to 100%")
    expect(editor.errors).to_contain_text("shortfall of 1")
    expect(editor.save_button).to_be_disabled()


@rebalancing("Validation", "TC-053", "AC-009b", "Nothing is saved after an invalid attempt")
def test_nothing_saved_after_invalid_input(
    rebalancing_page: RebalancingPage, api: ApiClient, user_with_flag
):
    rebalancing_page.open()
    rebalancing_page.start_new_model()
    editor = rebalancing_page.editor
    editor.set_name("Never saved")
    editor.add_asset_class(*EQUITY, weight=60)
    editor.add_asset_class(*FIXED_INCOME, weight=39)
    expect(editor.save_button).to_be_disabled()

    rebalancing_page.page.reload()
    expect(rebalancing_page.empty_state).to_be_visible()
    assert api.list_models(user_with_flag.auth_token).json() == []


@rebalancing("Validation", "TC-054", "AC-009b", "Errors clear once the input is fixed")
def test_errors_clear_after_fix(rebalancing_page: RebalancingPage):
    rebalancing_page.open()
    rebalancing_page.start_new_model()
    editor = rebalancing_page.editor
    editor.set_name("Fixed later")
    editor.add_asset_class(*EQUITY, weight=60)
    editor.add_asset_class(*FIXED_INCOME, weight=39)
    expect(editor.errors).to_be_visible()

    editor.set_weight("Fixed Income", 40)
    expect(editor.errors).to_have_count(0)
    expect(editor.save_button).to_be_enabled()

    editor.save()
    expect(rebalancing_page.model_select).to_contain_text("Fixed later")
