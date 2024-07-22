import pytest
import pandas as pd
from pyball.playerid_lookup import PlayerLookup

def test_playerid_lookup():
    client = PlayerLookup()

    # Test case 1: Lookup player by last name only
    result1 = client.search("Ramirez")
    assert isinstance(result1, pd.DataFrame)
    assert len(result1) > 0

    # Test case 2: Lookup player by last name and first name
    result2 = client.search("Ramirez", "Jose")
    assert isinstance(result2, pd.DataFrame)
    assert len(result2) > 0

    # Test case 3: Lookup player with non-existent last name
    result3 = client.search("NonExistentLastName")
    assert isinstance(result3, pd.DataFrame)
    assert len(result3) == 0

    # Test case 4: Lookup player with non-existent first name
    result4 = client.search("Doe", "NonExistentFirstName")
    assert isinstance(result4, pd.DataFrame)
    assert len(result4) == 0

    # Test case 5: Lookup player with both non-existent last name and first name
    result5 = client.search("doesn't", "exist", ignore_accents=True)
    assert isinstance(result5, pd.DataFrame)
    assert len(result5) == 0
