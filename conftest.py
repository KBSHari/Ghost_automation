import allure
import pytest
from playwright.sync_api import Page

from config import settings
from pages.portfolio_page import PortfolioPage
from pages.rebalancing_page import RebalancingPage
from utils.api_client import ApiClient, TestUser


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": True,
        "viewport": {"width": 1440, "height": 900},
    }


@pytest.fixture(scope="session")
def api() -> ApiClient:
    return ApiClient()


def sign_in(page: Page, user: TestUser) -> None:
    """Sign in through the app's own /auth/<jwt> route, as a real login would."""
    page.goto(f"{settings.BASE_URL}/{settings.LOCALE}/auth/{user.auth_token}")
    page.wait_for_url(lambda url: "/auth" not in url, timeout=60_000)


@pytest.fixture
def new_user(api: ApiClient):
    user = api.signup()
    yield user
    api.delete_user(user)


@pytest.fixture
def user_with_flag(api: ApiClient, new_user: TestUser) -> TestUser:
    api.set_experimental_features(new_user.auth_token, True)
    return new_user


@pytest.fixture
def signed_in_page(page: Page, user_with_flag: TestUser) -> Page:
    sign_in(page, user_with_flag)
    return page


@pytest.fixture
def signed_in_page_without_flag(page: Page, new_user: TestUser) -> Page:
    sign_in(page, new_user)
    return page


@pytest.fixture
def portfolio_page(signed_in_page: Page) -> PortfolioPage:
    return PortfolioPage(signed_in_page)


@pytest.fixture
def rebalancing_page(signed_in_page: Page) -> RebalancingPage:
    return RebalancingPage(signed_in_page)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the Allure report when a UI test fails."""
    outcome = yield
    report = outcome.get_result()
    page = item.funcargs.get("page") if hasattr(item, "funcargs") else None
    if report.when == "call" and report.failed and page is not None:
        try:
            allure.attach(
                page.screenshot(full_page=True),
                name="failure-screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception:
            pass
