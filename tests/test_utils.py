from pyball import utils


def test_utils():
    result1 = utils.make_bbref_player_url("ramirjo01")
    assert isinstance(result1, str)
    assert result1 == "https://www.baseball-reference.com/players/r/ramirjo01.shtml"

    result2 = utils.create_bbref_team_url("CLE", "2017")
    assert isinstance(result2, str)
    assert result2 == "https://www.baseball-reference.com/teams/CLE/2017.shtml"

    result3 = utils.make_savant_player_url("ramirez", "jose", "608070")
    assert isinstance(result3, str)
    assert result3 == "https://baseballsavant.mlb.com/savant-player/jose-ramirez-608070"
