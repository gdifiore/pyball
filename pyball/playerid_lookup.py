#
# File: playerid_lookup.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# (c) 2022-2024
#
# Description: File containing functions to obtain player (id) information from a lookup table
#              Modified to only gets name, baseball-reference/mlbam key and years played
#              Updated to new Github repo data source
#

import pandas as pd
import requests
import io
from functools import lru_cache

# Constants for the columns to keep in the dataframe
COLUMNS_TO_KEEP = [
    "name_last",
    "name_first",
    "key_bbref",
    "key_mlbam",
    "mlb_played_first",
    "mlb_played_last",
]

@lru_cache(maxsize=None)
def download_file(file_number):
    """
    Helper function to download a single file from the GitHub repository

    Parameters
    ----------
    file_number: int
        The file number to download

    Returns
    ----------
    pandas dataframe
        containing the data from the downloaded file
    """
    file = f"people-{file_number:x}.csv"  # incrementing hex number
    response = requests.get(
        f"https://raw.githubusercontent.com/chadwickbureau/register/master/data/{file}"
    )
    response.raise_for_status()  # raise HTTPError if the status code indicates an error
    return pd.read_csv(
        io.StringIO(response.content.decode("utf-8")),
        dtype={"key_sr_nfl": object, "key_sr_nba": object, "key_sr_nhl": object},
    )
    
@lru_cache(maxsize=1)
def get_lookup_table():
    """
    Function to download a lookup table of all players

    Returns
    ----------
    pandas dataframe
        containing the lookup table of all players
    """
    print("Gathering player lookup table. This may take a moment.")

    table = pd.DataFrame()
    file_number = 0
    while True:
        try:
            temp = download_file(file_number)
            table = pd.concat([table, temp], ignore_index=True)
            file_number += 1
        except requests.exceptions.HTTPError:
            break

    table = table[COLUMNS_TO_KEEP]
    table["name_last"] = table["name_last"].str.lower()
    table["name_first"] = table["name_first"].str.lower()
    return table

def playerid_lookup(last, first=None):
    """
    Function to lookup a player's baseball reference and mlbam id given their name, from the lookup table

    Parameters
    ----------
    last: String
        Last name of the player
    first: String, optional
        First name of the player

    Returns
    ----------
    pandas dataframe
        containing the player's name, baseball-reference id, mlbam id, and years played
    """
    last = last.lower()
    first = first.lower() if first else None

    table = get_lookup_table()

    query_string = f"name_last == '{last}'"
    query_string += f" and name_first == '{first}'" if first else ""
    results = table.query(query_string)

    return results.reset_index(drop=True)
