# qa-automation-portfolio
UI and API test automation with Python, pytest, Playwright and requests (automationexercise.com, restful-booker)

![tests](https://github.com/Halyna-Krokhtiak/qa-automation-portfolio/actions/workflows/tests.yml/badge.svg?branch=main)

## CI

Tests run automatically in GitHub Actions on every pull request and every push to `main`
(workflow: `.github/workflows/tests.yml`).

- API tests and UI tests run as separate steps; UI tests use `--reruns 2` because the demo site is sometimes overloaded.
- An HTML report (`reports/`) and Playwright screenshots, videos and traces for failed tests (`test-results/`)
  are uploaded as the `test-reports` artifact on every run, also when tests fail.
- To see results: Actions tab → latest run → Artifacts → `test-reports`.

## How to run UI tests with --reruns

Reruns help to run a failed test again in case of an unstable environment.

```
pytest tests/ui --reruns 2 --reruns-delay 5 -v
```

- `tests/ui` - run tests in the ui folder
- `--reruns 2` - if a test fails, try again up to 2 times
- `--reruns-delay 5` - wait 5 seconds between tries
