import allure

from config import settings


def rebalancing(story: str, tc: str, ac: str, title: str, severity=allure.severity_level.NORMAL):
    """Common Allure metadata so every report entry traces back to the QA plan and the ticket."""

    def decorator(func):
        for wrap in (
            allure.epic(settings.TICKET),
            allure.feature("Portfolio rebalancing"),
            allure.story(story),
            allure.title(f"{tc}: {title}"),
            allure.severity(severity),
            allure.tag(tc, ac),
            allure.link(f"{settings.JIRA_BASE_URL}/{settings.TICKET}", name=settings.TICKET),
        ):
            func = wrap(func)
        return func

    return decorator
