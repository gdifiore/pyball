import pandas as pd
from pyball.baseball_reference_player import BaseballReferencePlayerStatsScraper


def test_baseball_reference_player():
    url = "https://www.baseball-reference.com/players/a/aaronha01.shtml"
    scraper = BaseballReferencePlayerStatsScraper(url)
    batting_stats = scraper.batting_stats()
    assert isinstance(batting_stats, pd.DataFrame)
    assert len(batting_stats) > 0

    url = "https://www.baseball-reference.com/players/k/kershcl01.shtml"
    scraper = BaseballReferencePlayerStatsScraper(url)
    pitching_stats = scraper.pitching_stats()
    assert isinstance(pitching_stats, pd.DataFrame)
    assert len(pitching_stats) > 0