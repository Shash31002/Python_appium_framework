"""
DriverManager
-------------
Centralizes Appium driver creation and teardown, mirroring the role
DriverManager.java plays in the Selenium/Java framework: one place to
configure capabilities so tests never talk to Appium setup directly.
"""

from appium import webdriver
from appium.options.android import UiAutomator2Options

APPIUM_SERVER_URL = "http://127.0.0.1:4723"


def get_chrome_capabilities():
    """
    Capabilities to launch Google Chrome on an Android 17 device/emulator.
    Adjust deviceName/udid to match your local emulator or connected device.
    """
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = "17"
    options.automation_name = "UiAutomator2"
    options.device_name = "Android Emulator"
    options.app_package = "com.android.chrome"
    options.app_activity = "com.google.android.apps.chrome.Main"
    options.no_reset = True
    options.new_command_timeout = 120
    return options


class DriverManager:
    """Owns the single Appium driver instance for a test run."""

    _driver = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            options = get_chrome_capabilities()
            cls._driver = webdriver.Remote(APPIUM_SERVER_URL, options=options)
            cls._driver.implicitly_wait(10)
        return cls._driver

    @classmethod
    def quit_driver(cls):
        if cls._driver is not None:
            cls._driver.quit()
            cls._driver = None
