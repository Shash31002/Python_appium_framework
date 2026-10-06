"""
conftest.py
-----------
Shared pytest fixtures. The `driver` fixture plays the role of
@BeforeClass/@AfterClass in the Java/TestNG framework (setup + teardown
around each test). The pytest_html hooks below play the role of
TestListener.java - logging pass/fail and attaching context per test.
"""

import pytest
from utils.driver_manager import DriverManager


@pytest.fixture(scope="function")
def driver():
    """Provides a fresh Appium driver session per test, then quits after."""
    drv = DriverManager.get_driver()
    yield drv
    DriverManager.quit_driver()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Equivalent to TestListener.java's onTestSuccess/onTestFailure -
    logs each test's outcome and attaches it to the pytest-html report.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        status = "PASSED" if report.passed else "FAILED" if report.failed else "SKIPPED"
        print(f"[{status}] {item.name}")

        # Attach extra info to the HTML report if pytest-html is active
        if hasattr(item.config, "_html"):
            extra = getattr(report, "extra", [])
            report.extra = extra


def pytest_html_report_title(report):
    report.title = "Chrome on Android - Appium Test Report"
