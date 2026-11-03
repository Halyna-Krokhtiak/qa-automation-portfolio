# qa-automation-portfolio
UI and API test automation with Python, pytest, Playwright and requests (automationexercise.com, restful-booker)

## How to run UI tests with --reruns

Reruns help to run a failed test again in case of an unstable environment.

```
pytest tests/ui --reruns 2 --reruns-delay 5 -v
```

- `tests/ui` - run tests in the ui folder
- `--reruns 2` - if a test fails, try again up to 2 times
- `--reruns-delay 5` - wait 5 seconds between tries
