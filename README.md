# Ghost_automation

UI automation for Ghostfolio, written with Python, Playwright, the Page Object Model (POM) and Allure reporting.

First suite: **SCRUM-64 Portfolio rebalancing and target allocation planner** (UI scope only).

## Layout

```
config/settings.py          base URLs and locale (env: GHOSTFOLIO_URL, GHOSTFOLIO_API_URL, GHOSTFOLIO_LOCALE)
pages/                      Page Objects (no assertions): portfolio, rebalancing, model editor, result
utils/api_client.py         API helper used only for set-up and clean-up (users, settings, seed models)
conftest.py                 fixtures: a fresh user per test, sign-in via /auth/<jwt>, failure screenshots
tests/                      one file per area; every test carries its QA-plan ID as an Allure title and tag
```

Every test is titled `TC-xxx: ...` and tagged with its acceptance criterion, so the Allure report traces back to
`docs/artifacts/SCRUM-64/ph3b_qa_test_plan.md` in the Ghostfolio repo.

## Set-up

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

Allure reports need the Allure command line tool (https://allurereport.org/docs/install/).

## Run against a local Ghostfolio

The app must be running on **https://localhost:4200** (client; the Ghostfolio dev server uses HTTPS with a
self-signed certificate, which the tests accept) and http://localhost:3333 (API), with user sign-up enabled.
Every test creates its own throw-away user, so tests do not depend on each other or on existing data.

```
pytest                         # all tests, headless
pytest --headed --slowmo 300   # watch the browser
pytest -m smoke                # reachability checks only
pytest -m regression           # regression subset from the QA plan (TC-049, TC-059, TC-050)
pytest -m a11y                 # keyboard / accessible-name checks
```

Against another environment:

```
set GHOSTFOLIO_URL=https://your-host
set GHOSTFOLIO_API_URL=https://your-host
pytest
```

## Allure report

```
allure serve allure-results
```

Failed tests attach a full-page screenshot. Playwright traces: add `--tracing retain-on-failure`.

## Covered test cases (QA plan SCRUM-64)

| ID | Title | Marker |
|---|---|---|
| TC-049 | Rebalancing tab visible with the flag on | smoke, regression |
| TC-059 | Flag off hides the tab and the API returns 403 | smoke, regression |
| TC-050 | Create a model, run it, see the result | regression |
| TC-051 | Edit and delete a model | |
| TC-052 | Inline error when targets sum to 99% | |
| TC-053 | Nothing saved after an invalid attempt | |
| TC-054 | Errors clear once input is fixed | |
| TC-067 | Editor operable by keyboard | a11y |
| TC-068 | Editor controls have accessible names | a11y |

## Not covered yet

- TC-037 to TC-039 (trade table), TC-046 to TC-048 (CSV export): they need a portfolio with priced holdings.
  Seeding that data is the next step; it depends on a market-data provider or a manual asset profile in the target instance.
- TC-069 (translations): the new strings are not extracted into the locale files yet.
- API-layer cases (53 of the 69 planned) are outside this repo's UI scope.
