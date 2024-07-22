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

    Methods:
    --------
    batting_stats() -> Optional[pd.DataFrame]:
        Retrieves the batting statistics for the player.

    pitching_stats() -> Optional[pd.DataFrame]:
        Retrieves the pitching statistics for the player.
    """

    TABLE_IDS = {
        'batting': 'batting_standard',
        'pitching': 'pitching_standard'
    }

    def __init__(self, url: str):
        """
        Initializes a new instance of the BaseballReferencePlayerStatsScraper class.

        Parameters:
        -----------
        url : str
            The URL of the Baseball-Reference profile page for the player.

        Raises:
        -------
        ValueError:
            If the provided URL is invalid.
        """
        if not is_bbref_player_url(url):
            raise ValueError(f"Invalid player URL: {url}")
        self.url = url
        self.soup = self._get_soup()

    def _get_soup(self) -> Optional[BeautifulSoup]:
        """
        Retrieves the BeautifulSoup object for the player's profile page.

        Returns:
        --------
        Optional[BeautifulSoup]:
            The BeautifulSoup object representing the player's profile page, or None if retrieval failed.
        """
        soup = read_url(self.url)
        if soup is None:
            logger.warning("Failed to retrieve content from URL: %s", self.url)
        return soup

    def _find_table(self, table_id: str) -> Optional[BeautifulSoup]:
        """
        Finds the HTML table element with the specified ID.

        Parameters:
        -----------
        table_id : str
            The ID of the table to find.

        Returns:
        --------
        Optional[BeautifulSoup]:
            The BeautifulSoup object representing the found table, or None if not found.
        """
        return self.soup.find("table", id=self.TABLE_IDS[table_id])

    def _get_dataframe(self, table_id: str) -> Optional[pd.DataFrame]:
        """
        Parses the HTML table and returns it as a pandas DataFrame.

        Parameters:
        -----------
        table_id : str
            The ID of the table to parse.

        Returns:
        --------
        Optional[pd.DataFrame]:
            The parsed table as a pandas DataFrame, or None if parsing failed.
        """
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
        Retrieves the batting statistics for the player.

        Returns:
        --------
        Optional[pd.DataFrame]:
            The batting statistics for the player as a pandas DataFrame, or None if not available.
        """
        return self._get_dataframe('batting')

    def pitching_stats(self) -> Optional[pd.DataFrame]:
        """
        Retrieves the pitching statistics for the player.

        Returns:
        --------
        Optional[pd.DataFrame]:
            The pitching statistics for the player as a pandas DataFrame, or None if not available.
        """
        return self._get_dataframe('pitching')
