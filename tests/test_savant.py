import pytest
import pandas as pd
from pyball import savant


def test_savant():
    ohtani_batter = savant.SavantScraper(
        "https://baseballsavant.mlb.com/savant-player/shohei-ohtani-660271?stats=statcast-r-hitting-mlb"
    )
    ohtani_pitcher = savant.SavantScraper(
        "https://baseballsavant.mlb.com/savant-player/shohei-ohtani-660271?stats=statcast-r-pitching-mlb&playerType=pitcher"
    )

    result1 = ohtani_batter.get_percentile_stats()
    assert isinstance(result1, pd.DataFrame)
    assert len(result1) > 0

    result2 = ohtani_pitcher.get_pitching_stats()
    assert isinstance(result2, pd.DataFrame)
    assert len(result2) > 0

    result3 = ohtani_batter.get_batting_stats()
    assert isinstance(result3, pd.DataFrame)
    assert len(result3) > 0

    result4 = ohtani_pitcher.get_batted_ball_profile()
    assert isinstance(result4, pd.DataFrame)
    assert len(result4) > 0

    result5 = ohtani_batter.get_pitch_tracking()
    assert isinstance(result5, pd.DataFrame)
    assert len(result5) > 0
