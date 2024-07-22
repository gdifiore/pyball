import pytest
import pandas as pd
from pyball.baseball_reference_team import BaseballReferenceTeamStatsScraper

def test_baseball_reference_player():
    url = "https://www.baseball-reference.com/teams/LAD/2017.shtml"
    scraper = BaseballReferenceTeamStatsScraper(url)
    batting_stats = scraper.batting_stats()
    assert isinstance(batting_stats, pd.DataFrame)
    assert len(batting_stats) > 0

    pitching_stats = scraper.pitching_stats()
    assert isinstance(pitching_stats, pd.DataFrame)
    assert len(pitching_stats) > 0