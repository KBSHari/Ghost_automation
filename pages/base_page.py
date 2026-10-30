from playwright.sync_api import Page

from config import settings


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open_path(self, path: str) -> None:
        self.page.goto(f"{settings.BASE_URL}/{settings.LOCALE}{path}")
