"""
test_chrome_search.py
----------------------
Test class - equivalent to LoginTest.java. Contains @Test-style methods
and a data-provider (pytest's parametrize) that pulls from JSON via
JsonDataReader, deserialized into the SearchData model.
"""

import os
import pytest

from pages.chrome_search_page import ChromeSearchPage
from models.search_data import SearchData
from utils.json_data_reader import read_json_data

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "testdata", "search_data.json")


def load_search_cases():
    raw = read_json_data(DATA_FILE)
    return [SearchData.from_dict(item) for item in raw]


@pytest.mark.parametrize("case", load_search_cases(), ids=lambda c: c.query)
def test_chrome_search(driver, case):
    """
    Opens Chrome, enters a search query into the search box, submits it,
    and verifies the omnibox reflects the search (basic smoke assertion -
    extend with WebView/DOM assertions once results load, if needed).
    """
    search_page = ChromeSearchPage(driver)
    search_page.search(case.query)

    current_text = search_page.get_current_url_bar_text().lower()
    assert case.expected_contains.lower() in current_text or case.query.lower() in current_text, (
        f"Expected omnibox to reflect query '{case.query}', got '{current_text}'"
    )
