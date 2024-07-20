#
# File: playerid_lookup.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# (c) 2022-2024
#
# Description: File containing functions to obtain player (id) information from a lookup table
#              Modified to only gets name, baseball-reference/mlbam key and years played
#              Updated to new Github repo data source
#

from functools import lru_cache
import io
from typing import Optional
import logging
import requests
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlayerLookup:
    BASE_URL = "https://raw.githubusercontent.com/chadwickbureau/register/master/data/"
    COLUMNS_TO_KEEP = [
        "name_last",
        "name_first",
        "key_bbref",
        "key_mlbam",
        "mlb_played_first",
        "mlb_played_last",
    ]

    @staticmethod
    @lru_cache(maxsize=None)
    def download_file(file_number: int) -> pd.DataFrame:
        """
        Helper function to download a single file from the GitHub repository

        Parameters:
        -----------
        file_number: int
            The file number to download

        Returns:
        --------
        pd.DataFrame
            Containing the data from the downloaded file
        """
        file = f"people-{file_number:x}.csv"  # incrementing hex number
        url = f"{PlayerLookup.BASE_URL}{file}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return pd.read_csv(
                io.StringIO(response.content.decode("utf-8")),
                dtype={"key_sr_nfl": object, "key_sr_nba": object, "key_sr_nhl": object},
            )
        except requests.exceptions.HTTPError:
            logger.warning("File not found: %s", url)
            raise

    @staticmethod
    @lru_cache(maxsize=1)
    def get_lookup_table() -> pd.DataFrame:
        """
        Function to download a lookup table of all players

        Returns:
        --------
        pd.DataFrame
            Containing the lookup table of all players
        """
        logger.info("Gathering player lookup table. This may take a moment.")

        table = pd.DataFrame()
        file_number = 0
        while True:
            try:
                temp = PlayerLookup.download_file(file_number)
                table = pd.concat([table, temp], ignore_index=True)
                file_number += 1
            except requests.exceptions.HTTPError:
                break

        table = table[PlayerLookup.COLUMNS_TO_KEEP]
        table["name_last"] = table["name_last"].str.lower()
        table["name_first"] = table["name_first"].str.lower()
        return table

    @staticmethod
    def playerid_lookup(last: str, first: Optional[str] = None) -> pd.DataFrame:
        """
        Function to lookup a player's baseball reference and mlbam id given their name, from
        the lookup table

        Parameters:
        -----------
        last: str
            Last name of the player
        first: str, optional
            First name of the player

        Returns:
        --------
        pd.DataFrame
            Containing the player's name, baseball-reference id, mlbam id, and years played
        """
        last = last.lower()
        first = first.lower() if first else None

        table = PlayerLookup.get_lookup_table()

        query_string = f"name_last == '{last}'"
        query_string += f" and name_first == '{first}'" if first else ""
        results = table.query(query_string)

        return results.reset_index(drop=True)
