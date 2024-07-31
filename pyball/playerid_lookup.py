# File: playerid_lookup.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# (c) 2022-2024
#
# Description: File containing functions to obtain player (id) information
# on various statistic sites from a lookup table.

from functools import wraps
import io
import re
import diskcache
import zipfile
import unicodedata
import logging
import pandas as pd
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


cache = diskcache.Cache('./.pyball_cache')

def disk_cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = f"{func.__name__}:{args}:{kwargs}"
        result = cache.get(key)
        if result is None:
            result = func(*args, **kwargs)
            cache.set(key, result)
        return result
    return wrapper

class PlayerLookup:
    """
    A class for looking up player information in the registry.

    Attributes:
        REGISTRY_URL (str): The URL of the player registry.
        CSV_FILE_PATTERN (re.Pattern): The regular expression pattern for matching CSV file names.

    Methods:
        fetch_chadwick_data: Fetches and processes player data from the Chadwick Register.
        load_player_registry: Loads and preprocesses the player registry.
        remove_accents: Removes accents marks from a given string.
        search: Searches for a player in the registry based on their name.
    """
    REGISTRY_URL = "https://github.com/chadwickbureau/register/archive/refs/heads/master.zip"
    CSV_FILE_PATTERN = re.compile("/people.+csv$")

    def __init__(self):
        self.registry = self.load_player_registry()

    @staticmethod
    def _find_csv_files(zip_archive: zipfile.ZipFile):
        return [
            file for file in zip_archive.infolist()
            if re.search(PlayerLookup.CSV_FILE_PATTERN, file.filename)
        ]

    @staticmethod
    def _compile_player_data(zip_archive: zipfile.ZipFile) -> pd.DataFrame:
        dataframes = [
            pd.read_csv(io.BytesIO(zip_archive.read(csv_file.filename)), low_memory=False)
            for csv_file in PlayerLookup._find_csv_files(zip_archive)
        ]
        return pd.concat(dataframes, axis=0)

    @staticmethod
    @disk_cache
    def fetch_chadwick_data() -> pd.DataFrame:
        """
        Fetches and processes player data from the Chadwick Register.

        Returns:
            pd.DataFrame: A DataFrame containing player data from the Chadwick Register.
        """
        logger.info('Fetching player registry. This may take a moment.')
        response = requests.get(PlayerLookup.REGISTRY_URL, timeout=10)
        zip_content = io.BytesIO(response.content)

        mlb_columns = ['key_retro', 'key_bbref', 'key_fangraphs', 'mlb_played_first', 'mlb_played_last']
        essential_columns = ['name_last', 'name_first', 'key_mlbam'] + mlb_columns

        with zipfile.ZipFile(zip_content) as archive:
            data = PlayerLookup._compile_player_data(archive)[essential_columns]

        # Filter for MLB players and clean data
        data = data.dropna(how='all', subset=mlb_columns).reset_index(drop=True)
        data[['key_mlbam', 'key_fangraphs']] = data[['key_mlbam', 'key_fangraphs']].fillna(-1).astype(int)

        return data

    @staticmethod
    def load_player_registry():
        """
        Loads and preprocesses the player registry.

                Returns:
            pandas.DataFrame: The preprocessed player registry.
        """
        registry = PlayerLookup.fetch_chadwick_data()
        registry[['name_last', 'name_first']] = registry[['name_last', 'name_first']].apply(lambda x: x.str.lower())
        return registry

    @staticmethod
    def remove_accents(text: str) -> str:
        """
        Removes accents marks from a given string.

        Args:
                text (str): The input string from which accents marks will be removed.

        Returns:
            str: The input string without any accents marks.
        """
        normalized = unicodedata.normalize('NFD', str(text))
        return ''.join(char for char in normalized if unicodedata.category(char) != 'Mn')

    def search(self, last_name: str, first_name: str = None, ignore_accents: bool = True) -> pd.DataFrame:
        """
        Searches for a player in the registry based on their name.

        Parameters:
        - last_name (str): The last name of the player to search for.
        - first_name (str, optional): The first name of the player to search for. Defaults to None.
        - ignore_accents (bool, optional): Whether to ignore accents in the search. Defaults to True.

        Returns:
        - pd.DataFrame: A DataFrame containing the search results.
        """
        last_name = last_name.lower()
        first_name = first_name.lower() if first_name else None

        if ignore_accents:
            last_name = self.remove_accents(last_name)
            first_name = self.remove_accents(first_name) if first_name else None
            self.registry['name_last'] = self.registry['name_last'].apply(self.remove_accents)
            self.registry['name_first'] = self.registry['name_first'].apply(self.remove_accents)

        if first_name:
            results = self.registry[(self.registry['name_last'] == last_name) & (self.registry['name_first'] == first_name)]
        else:
            results = self.registry[self.registry['name_last'] == last_name]

        return results.reset_index(drop=True)
