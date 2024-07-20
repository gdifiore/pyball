#
# File: baseball_reference_player.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# (c) 2022-2024
#
# Description: File containing functions to obtain player stats from Baseball-Reference
#

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

    Private Methods:
    ----------------
    _find_batting_table(soup: BeautifulSoup) -> Optional[BeautifulSoup]:
        Locates the batting statistics table in the parsed HTML.
    _find_pitching_table(soup: BeautifulSoup) -> Optional[BeautifulSoup]:
        Locates the pitching statistics table in the parsed HTML.

    Note:
    -----
    This class relies on the structure of Baseball-Reference pages as of 2024.
    Changes to the website structure may affect the functionality of this scraper.
    """
    PLAYER_BATTING_TABLE_ID = "batting_standard"
    PLAYER_PICHING_TABLE_ID = "pitching_standard"

    @staticmethod
    def _find_batting_table(soup: BeautifulSoup) -> Optional[BeautifulSoup]:
        """
        Find the batting stats table (Baseball-Reference) in the soup

        Parameters:
        -----------
        soup: BeautifulSoup
            Contains the html of the player page

        Returns:
        --------
        Optional[BeautifulSoup]
            Contains the html of the batting stats table, or None if not found
        """
        return soup.find("table", id=BaseballReferencePlayerStatsScraper.PLAYER_BATTING_TABLE_ID)

    @staticmethod
    def batting_stats(url: str) -> Optional[pd.DataFrame]:
        """
        Return the (Baseball-Reference) batting stats for a player as a pandas dataframe

        Parameters:
        -----------
        url: str
            URL of the player page

        Returns:
        --------
        Optional[pd.DataFrame]
            Contains the batting stats for the player, or None if not available
        """
        if not is_bbref_player_url(url):
            logger.warning("Invalid player URL: %s", url)
            return None

        soup = read_url(url)
        if soup is None:
            logger.warning("Failed to retrieve content from URL: %s", url)
            return None

        table = BaseballReferencePlayerStatsScraper._find_batting_table(soup)
        if table is None:
            logger.warning("Batting stats table not found for URL: %s", url)
            return None

        try:
            df = pd.read_html(str(table))[0]
            return df.dropna(how="all")
        except ValueError as e:
            logger.error("Error parsing batting stats table (no tables found): %s", str(e))
            return None
        except Exception as e:
            logger.error("Error parsing batting stats table: %s", str(e))
            return None

    @staticmethod
    def _find_pitching_table(soup):
        """
        Function to find the pitching stats table (Baseball-Reference) in the soup

        Parameters
        ----------
        soup: BeautifulSoup object
            Contains the html of the player page

        Returns
        ----------
        BeautifulSoup object
            Contains the html of the pitching stats table
        """
        return soup.find("table", id=BaseballReferencePlayerStatsScraper.PLAYER_PICHING_TABLE_ID)

    @staticmethod
    def pitching_stats(url: str) -> Optional[pd.DataFrame]:
        """
        Return the (Baseball-Reference) pitching stats for a player as a pandas dataframe

        Parameters:
        -----------
        url: str
            URL of the player page

        Returns:
        --------
        Optional[pd.DataFrame]
            Contains the pitching stats for the player, or None if not available
        """
        if not is_bbref_player_url(url):
            logger.warning("Invalid player URL: %s", url)
            return None

        soup = read_url(url)
        if soup is None:
            logger.warning("Failed to retrieve content from URL: %s", url)
            return None

        table = BaseballReferencePlayerStatsScraper._find_pitching_table(soup)
        if table is None:
            logger.warning("Pitching stats table not found for URL: %s", url)
            return None

        try:
            df = pd.read_html(str(table))[0]
            return df.dropna(how="all")
        except ValueError as e:
            logger.error("Error parsing pitching stats table (no tables found): %s", str(e))
            return None
        except Exception as e:
            logger.error("Unexpected error parsing pitching stats table: %s", str(e))
            return None
