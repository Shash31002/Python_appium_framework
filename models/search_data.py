"""
SearchData
----------
Typed data model for a single search test case, mirroring the role
LoginData.java plays as a POJO for JSON-driven test data.
"""

from dataclasses import dataclass


@dataclass
class SearchData:
    query: str
    expected_contains: str

    @staticmethod
    def from_dict(d):
        return SearchData(
            query=d["query"],
            expected_contains=d["expected_contains"],
        )
