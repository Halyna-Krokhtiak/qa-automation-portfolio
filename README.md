# qa-automation-portfolio

![tests](https://github.com/Halyna-Krokhtiak/qa-automation-portfolio/actions/workflows/tests.yml/badge.svg?branch=main)

Test automation project in Python: UI tests for the automationexercise.com web shop (Playwright + Page Object Model) and API tests for the restful-booker REST API (requests). 43 test cases (25 UI + 18 API), run in GitHub Actions on every push and pull request.

## What is tested

### UI — automationexercise.com

Login — valid login, invalid login (wrong password, unregistered email, empty password), logout.
Search — search by product name, case-insensitive search, "Searched Products" title, no results for an unknown query.
Cart — add a product to cart, add two different products, add the same product twice, total price in cart depends on quantity, remove a product from cart.
Checkout — place an order (e2e), checkout delivery address matches the user's data, guest user on checkout is asked to log in, payment with an empty card is blocked, cart is empty after the order.

Test users are created via the site API before a test and deleted after it, so UI tests do not depend on each other.

### API — restful-booker

CRUD — create a booking, get a new booking by id, update (PUT) user name for existing booking, delete a booking, get the list of booking ids.
Auth — valid login returns a token; invalid credentials return no token.
Negative cases — 404 for non-existent ids (0, 999999999, "abc"), 403 for update without a token.

## Tech stack

Python language - version 3.13;
pytest — test runner, fixtures, parametrization;
Playwright (pytest-playwright) — browser automation for UI tests;
requests — HTTP client for API tests and test data setup;
pytest-html — HTML test reports;
pytest-rerunfailures — reruns for flaky UI tests;
flake8 — code style check (PEP 8);
GitHub Actions — CI.

## Project structure
```
pages/               # Page Objects: locators and actions for each site page
  base_page.py       #   common logic (base URL, open())
tests/
  api/               # API tests for restful-booker
  ui/                # UI tests for automationexercise.com
    conftest.py      #   UI fixtures: ad blocking, cookie banner, test user via API, logged-in user
conftest.py          # API fixtures: new booking, auth token, auth headers
config.py            # API base URL and credentials (can be set via env variables)
pytest.ini           # Playwright options: screenshot / video / trace on failure
requirements.txt     # dependencies
.github/workflows/   # CI workflow
```

## How to run
```bash

git clone https://github.com/Halyna-Krokhtiak/qa-automation-portfolio.git
cd qa-automation-portfolio

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
playwright install chromium

pytest                             # all tests
pytest tests/api -v                # API tests only
pytest tests/ui -v                 # UI tests only (headless)
pytest tests/ui --headed           # UI tests with a visible browser
pytest tests/ui --reruns 2 --reruns-delay 5    # retry failed UI tests up to 2 times, 5 s between tries
pytest --html=reports/report.html --self-contained-html   # with an HTML report
```

## Test reports

HTML report — add --html=reports/report.html --self-contained-html, then open the file in a browser.
Screenshots, videos, traces — saved to test-results/ only for failed tests (configured in pytest.ini). Open a trace with playwright show-trace test-results/<test-name>/trace.zip.
In CI — Actions tab → a workflow run → Artifacts → test-reports (contains reports/api.html, reports/ui.html and test-results/). Kept for 14 days.

## CI

Tests run automatically in GitHub Actions on every pull request and every push to `main`
(workflow: `.github/workflows/tests.yml`).

- API tests and UI tests run as separate steps; UI tests use `--reruns 2` because the demo site is sometimes overloaded.
- An HTML report (`reports/`) and Playwright screenshots, videos and traces for failed tests (`test-results/`)
  are uploaded as the `test-reports` artifact on every run, also when tests fail.
- To see results: Actions tab → latest run → Artifacts → `test-reports`.

## Known issues / found bugs

Tests marked xfail document real behaviour that differs from what is expected:

API: POST /auth with invalid credentials - 200 OK with {"reason": "Bad credentials"} (xfail; the actual behaviour is covered by a separate test). Expected: 401 Unauthorized.

UI: search for "Top" - "Little Girls Mr. Panda Shirt" is returned because it is in the Tops category — search also matches by category (xfail). Expected: every result contains "top" in the name.

Other restful-booker specifics that the tests check as they are:

GET /ping returns 201 Created instead of 200 OK
DELETE /booking/{id} returns 201 Created instead of 200 / 204
update without a token returns 403 Forbidden, not 401 Unauthorized
