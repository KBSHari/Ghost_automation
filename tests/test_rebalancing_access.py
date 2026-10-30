import allure
import pytest
import requests
from playwright.sync_api import expect

from config import settings
from pages.portfolio_page import PortfolioPage
from pages.rebalancing_page import RebalancingPage
from tests.allure_tags import rebalancing

CRITICAL = allure.severity_level.CRITICAL


@pytest.mark.smoke
@pytest.mark.regression
@rebalancing("Access", "TC-049", "AC-009a", "Rebalancing tab is visible with the flag on", CRITICAL)
def test_tab_visible_with_flag_on(portfolio_page: PortfolioPage):
    portfolio_page.open()

    expect(portfolio_page.rebalancing_tab).to_be_visible()
    # The existing tabs must be unchanged
    for name in ("Allocations", "Analysis", "FIRE", "X-ray"):
        expect(portfolio_page.tab(name)).to_be_visible()

    portfolio_page.open_rebalancing_tab()
    expect(portfolio_page.page).to_have_url(
        f"{settings.BASE_URL}/{settings.LOCALE}/portfolio/rebalancing"
    )
    expect(RebalancingPage(portfolio_page.page).heading).to_be_visible()


@pytest.mark.smoke
@pytest.mark.regression
@rebalancing("Access", "TC-059", "AC-011a", "Flag off hides the tab and the API denies access", CRITICAL)
def test_tab_hidden_and_api_denied_with_flag_off(signed_in_page_without_flag, new_user):
    page = signed_in_page_without_flag
    portfolio_page = PortfolioPage(page).open()

    expect(portfolio_page.tab("Analysis")).to_be_visible()
    expect(portfolio_page.rebalancing_tab).to_have_count(0)

    with allure.step("The API refuses the new routes with 403"):
        response = requests.get(
            f"{settings.API_URL}/api/v1/rebalancing/models",
            headers={"Authorization": f"Bearer {new_user.auth_token}"},
            timeout=30,
        )
        assert response.status_code == 403
