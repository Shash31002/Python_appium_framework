"""
JsonDataReader
--------------
Reads external JSON test data files, keeping test data decoupled from
test logic - mirrors JsonDataReader.java from the Selenium/Java framework.
"""

import json
import os


def read_json_data(file_path):
    """Returns the parsed contents of a JSON test data file as a Python object."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Test data file not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
