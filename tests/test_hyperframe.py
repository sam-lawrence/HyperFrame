import gzip
import json

import pandas as pd
from bs4 import BeautifulSoup
from pandas._testing import assert_frame_equal

from hyperframe.hyperpattern import HyperPatternHunter

EXPECTED_HYPERFRAMES_PATH = "tests/fixtures/beauhurst_expected_hyperframe_fixture.json"
BEAUHURST_HTML_PATH = "tests/fixtures/beauhurst_scrapedpage_html.gz"


def get_expected_hyperframes() -> list[pd.DataFrame]:
    expected_hyperframes = []
    with open(EXPECTED_HYPERFRAMES_PATH) as fd:
        fixture_data = json.load(fd)
        for frame_data, frame_columns in zip(
            fixture_data["data"],
            fixture_data["columns"],
        ):
            # hyperframe columns are tuples, not lists (thanks json)
            columns = [tuple(col) for col in frame_columns]
            expected_hyperframes.append(pd.DataFrame(frame_data, columns=columns))
    return expected_hyperframes


def get_beauhurst_html_soup() -> BeautifulSoup:
    with gzip.open(BEAUHURST_HTML_PATH, "r") as fd:
        html = fd.read()
    return BeautifulSoup(html, "lxml")


def test_hyperframes_from_page() -> None:
    # Get the beauhurst website html fixture as soup
    beauhurst_soup = get_beauhurst_html_soup()

    # Get the expected hyperframe fixture
    expected_hyperframes = get_expected_hyperframes()

    # Extract hyperframes from the soup
    pattern_hunter = HyperPatternHunter(beauhurst_soup)
    hyperframes = [
        hyperpattern.get_hyperframe()
        for hyperpattern in pattern_hunter.yield_hyperpatterns()
    ]

    # Assert we have the correct number of hyperframes
    assert len(hyperframes) == len(expected_hyperframes)

    # Assert we have the correct hyperframes
    for idx in range(len(hyperframes)):
        assert_frame_equal(hyperframes[idx], expected_hyperframes[idx])
