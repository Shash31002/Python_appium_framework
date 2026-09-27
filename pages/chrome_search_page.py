"""
ChromeSearchPage
-----------------
Page Object for the Chrome app's search bar (omnibox), same role as
LoginPage.java: locators + actions only, no assertions here.
"""

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ChromeSearchPage:

    # Locators
    NEW_TAB_SEARCH_BOX = (AppiumBy.ID, "com.android.chrome:id/search_box_text")
    OMNIBOX_URL_BAR = (AppiumBy.ID, "com.android.chrome:id/url_bar")
    ACCEPT_TOS_BUTTON = (AppiumBy.ID, "com.android.chrome:id/terms_accept")
    NO_THANKS_SIGNIN_BUTTON = (AppiumBy.ID, "com.android.chrome:id/negative_button")

    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def dismiss_first_run_dialogs_if_present(self):
        """Handles Chrome's first-launch ToS / sign-in prompts, if shown."""
        for locator in (self.ACCEPT_TOS_BUTTON, self.NO_THANKS_SIGNIN_BUTTON):
            try:
                el = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(locator))
                el.click()
            except Exception:
                pass  # dialog not shown - safe to continue

    def tap_search_box(self):
        el = self.wait.until(EC.element_to_be_clickable(self.NEW_TAB_SEARCH_BOX))
        el.click()

    def enter_search_text(self, text):
        el = self.wait.until(EC.presence_of_element_located(self.OMNIBOX_URL_BAR))
        el.clear()
        el.send_keys(text)

    def submit_search(self):
        self.driver.press_keycode(66)  # Android ENTER keycode

    def search(self, query):
        """Full flow: tap search box, type query, submit."""
        self.dismiss_first_run_dialogs_if_present()
        self.tap_search_box()
        self.enter_search_text(query)
        self.submit_search()

    def get_current_url_bar_text(self):
        el = self.wait.until(EC.presence_of_element_located(self.OMNIBOX_URL_BAR))
        return el.text
