# Selenium Pytest Framework

A UI and API test automation framework built with Selenium and pytest, featuring the Page Object Model, Allure reporting, and a GitHub Actions CI/CD pipeline.

---

## Project Structure

```
selenium-pytest-framework/
├── pages/              # Page Object Model classes
│   ├── base_page.py
│   ├── login_page.py
│   └── secure_area_page.py
├── tests/              # Test suites
│   ├── test_login.py
│   └── test_api_users.py
├── utils/              # Shared utilities
│   ├── config.py       # Central configuration
│   ├── api_client.py   # REST API client (ReqRes)
│   ├── data_loader.py  # JSON test-data loader
│   └── driver_factory.py  # WebDriver creation
├── test_data/          # External test data (JSON)
│   ├── login_data.json
│   └── api_users.json
├── conftest.py         # Shared pytest fixtures and hooks
├── pytest.ini          # Pytest configuration
└── requirements.txt    # Pinned dependencies
```

---

## Prerequisites

- Python 3.11+
- Chrome / Firefox / Safari (depending on target browser)
- `pip install -r requirements.txt`

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BROWSER` | `safari` | Browser to use: `chrome`, `firefox`, or `safari` |
| `BASE_TIMEOUT` | `10` | Selenium wait timeout in seconds |
| `REQRES_API_KEY` | _(none)_ | API key from [app.reqres.in/api-keys](https://app.reqres.in/api-keys) — required for API tests |
| `CI` | _(none)_ | Set automatically by GitHub Actions; enables headless mode |

---

## Running Tests

### All tests
```bash
pytest
```

### By marker
```bash
pytest -m smoke            # Smoke tests only
pytest -m regression       # Regression tests only
pytest -m api              # API tests only (requires REQRES_API_KEY)
pytest -m "smoke or regression"  # UI tests
```

### Specific browser
```bash
BROWSER=chrome pytest -m "smoke or regression"
BROWSER=firefox pytest -m "smoke or regression"
```

### With Allure reporting
```bash
pytest --alluredir=allure-results
allure serve allure-results
```

### Parallel execution (API tests)
```bash
pytest -m api -n auto
```

---

## Retry Logic

Flaky tests automatically retry up to **2 times** with a 1-second delay (configured in `pytest.ini` via `pytest-rerunfailures`). To disable retries locally:

```bash
pytest -p no:rerunfailures
```

---

## Screenshots

Failed UI tests automatically save screenshots to `screenshots/<test_name>.png`. This directory is excluded from git.

---

## CI/CD

GitHub Actions runs three parallel jobs on every push/PR to `main`:

| Job | Runner | Marker |
|-----|--------|--------|
| API tests | ubuntu-latest | `api` |
| UI tests (Chrome) | ubuntu-latest | `smoke or regression` |
| UI tests (Safari) | macos-latest | `smoke or regression` |

The Allure report is deployed to **GitHub Pages** only when both the API and Chrome UI jobs succeed.

---

## Test Data

All test data lives in `test_data/` as JSON files and is loaded via `utils/data_loader.py`.

- `login_data.json` — valid credentials and parameterized invalid-login cases
- `api_users.json` — payloads for create/update user API tests

---

## Adding New Tests

1. Create a page object in `pages/` extending `BasePage`.
2. Add test data to `test_data/` if needed.
3. Write tests in `tests/test_<feature>.py` using the `driver` fixture.
4. Mark tests with `@pytest.mark.smoke`, `@pytest.mark.regression`, or `@pytest.mark.api`.
