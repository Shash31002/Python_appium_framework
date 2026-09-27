# Chrome on Android - Appium Test Automation Framework

A Python + Appium + Pytest automation framework for testing the Google Chrome
app on Android (target: Android 17), built with the **Page Object Model**
and JSON-driven test data. Structured to mirror an existing Selenium/Java/
TestNG framework, so the same mental model applies across both.

## Overview

This framework launches the Chrome app on an Android device/emulator via
Appium, interacts with the search box (omnibox), and verifies search input
is accepted correctly - driven by external JSON test data rather than
hardcoded values.

## Tech Stack

| Tool / Library          | Purpose                                           |
|---------------------------|----------------------------------------------------|
| Python                   | Core language                                       |
| Appium-Python-Client      | Mobile automation - drives the app via Appium server |
| UiAutomator2              | Android automation engine (Appium driver backend)   |
| Pytest                    | Test runner, fixtures, parametrized data-provider   |
| pytest-html                | HTML test execution reports                        |
| Selenium (WebDriverWait)   | Explicit waits / expected_conditions               |

## Project Structure

```
appium-chrome-framework/
 ├── pages/
 │    └── chrome_search_page.py   → Page Object: locators + actions for the search box
 ├── models/
 │    └── search_data.py          → Typed data model (mirrors a POJO)
 ├── utils/
 │    ├── driver_manager.py       → Appium driver lifecycle (capabilities, create/quit)
 │    └── json_data_reader.py     → Reads JSON test data files
 ├── tests/
 │    └── test_chrome_search.py   → Test cases + data-driven parametrize
 ├── testdata/
 │    └── search_data.json        → External test data (search queries)
 ├── reports/
 │    └── report.html             → Generated after each run (pytest-html)
 ├── conftest.py                  → Pytest fixtures (setup/teardown) + report hooks
 ├── pytest.ini                   → Pytest + report configuration
 └── requirements.txt
```

## Design Approach (mirrors the Java/Selenium framework)

| Concept                  | Java/Selenium version         | This framework                      |
|---------------------------|-------------------------------|--------------------------------------|
| Page Object                | `LoginPage.java`               | `pages/chrome_search_page.py`         |
| Data model / POJO           | `LoginData.java`                | `models/search_data.py` (dataclass)   |
| JSON reading                | `JsonDataReader.java` (Jackson) | `utils/json_data_reader.py`           |
| Driver lifecycle             | `DriverManager.java`            | `utils/driver_manager.py`             |
| Test class + data-provider   | `LoginTest.java` + `@DataProvider` | `test_chrome_search.py` + `@pytest.mark.parametrize` |
| Setup/teardown               | `@BeforeClass` / `@AfterClass`  | `driver` pytest fixture               |
| Listener / reporting hook     | `TestListener.java`             | `conftest.py` pytest hooks + pytest-html |
| Suite config                  | `testng.xml`                    | `pytest.ini`                          |

## Prerequisites

1. **Appium Server** running locally (or remotely):
   ```bash
   npm install -g appium
   appium driver install uiautomator2
   appium
   ```
2. **Android SDK** + an emulator (Android 17) or a physical device with
   USB debugging enabled, and Chrome installed.
3. Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Update device/emulator details in `utils/driver_manager.py` if needed:
```python
options.device_name = "Android Emulator"   # match your AVD/device name
options.platform_version = "17"
```

## Running Tests

```bash
pytest
```

This uses the `addopts` in `pytest.ini`, which automatically generates
an HTML report at:
```
reports/report.html
```

Run a specific test file:
```bash
pytest tests/test_chrome_search.py
```

## Sample Test Flow

```
search_data.json → JsonDataReader → SearchData (model) → @parametrize → test_chrome_search
```

`test_chrome_search` uses `ChromeSearchPage` to tap the search box, enter
the query, submit it, and assert the omnibox reflects the expected text.

## Future Improvements

- Add gesture handling utilities (swipe/scroll) for scrolling search results
- Externalize device capabilities into a `config.json` / `config.yaml` for
  multi-device / CI (emulator farm) runs
- Add CI integration (GitHub Actions/Jenkins) running against a cloud
  device farm (e.g. BrowserStack/Sauce Labs) since Appium needs a real
  Android environment, unlike a headless browser
- Add screenshot-on-failure, attached to the pytest-html report
