# File: playerid_lookup.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# (c) 2022-2024
#
# Description: File containing functions to obtain player (id) information from a lookup table
#              Modified to only gets name, baseball-reference/mlbam key and years played
#              Updated to new Github repo data source

import io
import re
import zipfile
from typing import List, Tuple
import pandas as pd
import requests
from functools import lru_cache
import unicodedata
from difflib import get_close_matches

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlayerLookup:
    BASE_URL = "https://github.com/chadwickbureau/register/archive/refs/heads/master.zip"
    PEOPLE_FILE_PATTERN = re.compile("/people.+csv$")

    def __init__(self):
        self.table = self.get_lookup_table()

    @staticmethod
    def _extract_people_files(zip_archive: zipfile.ZipFile):
        return filter(
            lambda zip_info: re.search(PlayerLookup.PEOPLE_FILE_PATTERN, zip_info.filename),
            zip_archive.infolist(),
        )

    @staticmethod
    def _extract_people_table(zip_archive: zipfile.ZipFile) -> pd.DataFrame:
        dfs = map(
            lambda zip_info: pd.read_csv(
                io.BytesIO(zip_archive.read(zip_info.filename)),
                low_memory=False
            ),
            PlayerLookup._extract_people_files(zip_archive),
        )
        return pd.concat(dfs, axis=0)

    @staticmethod
    @lru_cache(maxsize=1)
    def chadwick_register() -> pd.DataFrame:
        logger.info('Gathering player lookup table. This may take a moment.')
        s = requests.get(PlayerLookup.BASE_URL).content
        mlb_only_cols = ['key_retro', 'key_bbref', 'key_fangraphs', 'mlb_played_first', 'mlb_played_last']
        cols_to_keep = ['name_last', 'name_first', 'key_mlbam'] + mlb_only_cols
        table = PlayerLookup._extract_people_table(
            zipfile.ZipFile(io.BytesIO(s))
        ).loc[:, cols_to_keep]

        table.dropna(how='all', subset=mlb_only_cols, inplace=True)  # Keep only the major league rows
        table.reset_index(inplace=True, drop=True)

        table[['key_mlbam', 'key_fangraphs']] = table[['key_mlbam', 'key_fangraphs']].fillna(-1)
        table[['key_mlbam', 'key_fangraphs']] = table[['key_mlbam', 'key_fangraphs']].astype(int)

        return table[cols_to_keep]

    @staticmethod
    def get_lookup_table():
        table = PlayerLookup.chadwick_register()
        table['name_last'] = table['name_last'].str.lower()
        table['name_first'] = table['name_first'].str.lower()
        return table

    @staticmethod
    def normalize_accents(s: str) -> str:
        return ''.join(c for c in unicodedata.normalize('NFD', str(s)) if unicodedata.category(c) != 'Mn')

    @staticmethod
    def get_closest_names(last: str, first: str, player_table: pd.DataFrame) -> pd.DataFrame:
        filled_df = player_table.fillna("").assign(chadwick_name=lambda row: row.name_first + " " + row.name_last)
        fuzzy_matches = pd.DataFrame(
            get_close_matches(f"{first} {last}", filled_df.chadwick_name, n=5, cutoff=0)
        ).rename({0: "chadwick_name"}, axis=1)
        return fuzzy_matches.merge(filled_df, on="chadwick_name").drop("chadwick_name", axis=1)

    def search(self, last: str, first: str = None, fuzzy: bool = False, ignore_accents: bool = False) -> pd.DataFrame:
        last = last.lower()
        first = first.lower() if first else None

        if ignore_accents:
            last = self.normalize_accents(last)
            first = self.normalize_accents(first) if first else None
            self.table['name_last'] = self.table['name_last'].apply(self.normalize_accents)
            self.table['name_first'] = self.table['name_first'].apply(self.normalize_accents)

        if first is None:
            results = self.table.loc[self.table['name_last'] == last]
        else:
            results = self.table.loc[(self.table['name_last'] == last) & (self.table['name_first'] == first)]

        results = results.reset_index(drop=True)

        if len(results) == 0 and fuzzy:
            logger.info("No identically matched names found! Returning the 5 most similar names.")
            results = self.get_closest_names(last=last, first=first, player_table=self.table)

        return results
