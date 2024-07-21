# File: baseball_reference_player.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# (c) 2022-2024
#
# Description: File containing functions to obtain player stats from Baseball-Reference

from typing import Optional
import logging
import pandas as pd
from bs4 import BeautifulSoup

from pyball.utils import read_url, is_bbref_player_url

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseballReferencePlayerStatsScraper:
    """
    A class for scraping player statistics from Baseball-Reference.

    This class provides methods to extract batting and pitching statistics
    for baseball players from their Baseball-Reference profile pages.

    Attributes:
    -----------
    PLAYER_BATTING_TABLE_ID : str
        The HTML id of the table containing batting statistics on Baseball-Reference.
    PLAYER_PITCHING_TABLE_ID : str
        The HTML id of the table containing pitching statistics on Baseball-Reference.

    Methods:
    --------
    batting_stats(url: str) -> Optional[pd.DataFrame]:
        Retrieves the batting statistics for a player from the given URL.
    pitching_stats(url: str) -> Optional[pd.DataFrame]:
        Retrieves the pitching statistics for a player from the given URL.
    """
    TABLE_IDS = {
        'batting': 'batting_standard',
        'pitching': 'pitching_standard'
    }

    def __init__(self, url: str):
        if not is_bbref_player_url(url):
            raise ValueError(f"Invalid player URL: {url}")
        self.url = url
        self.soup = self._get_soup()

    def _get_soup(self) -> Optional[BeautifulSoup]:
        soup = read_url(self.url)
        if soup is None:
            logger.warning("Failed to retrieve content from URL: %s", self.url)
        return soup

    def _find_table(self, table_id: str) -> Optional[BeautifulSoup]:
        return self.soup.find("table", id=self.TABLE_IDS[table_id])

    def _get_dataframe(self, table_id: str) -> Optional[pd.DataFrame]:
        table = self._find_table(table_id)
        if table is None:
            logger.warning("%s stats table not found for URL: %s", table_id.capitalize(), self.url)
            return None

        try:
            df = pd.read_html(str(table))[0]
            return df.dropna(how="all")
        except ValueError as e:
            logger.error("Error parsing %s stats table (no tables found): %s", table_id, str(e))
            return None
        except Exception as e:
            logger.error("Error parsing %s stats table: %s", table_id, str(e))
            return None

    def batting_stats(self) -> Optional[pd.DataFrame]:
        """
        Return the (Baseball-Reference) batting stats for a player as a pandas dataframe

        Returns:
        --------
        Optional[pd.DataFrame]
            Contains the batting stats for the player, or None if not available
        """
        return self._get_dataframe('batting')

    def pitching_stats(self) -> Optional[pd.DataFrame]:
        """
        Return the (Baseball-Reference) pitching stats for a player as a pandas dataframe

        Returns:
        --------
        Optional[pd.DataFrame]
            Contains the pitching stats for the player, or None if not available
        """
        return self._get_dataframe('pitching')
