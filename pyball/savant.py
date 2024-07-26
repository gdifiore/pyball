# File: savant.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# (c) 2022-2024
#
# Description: File containing functions to obtain player savant data

from typing import Optional
import logging
import pandas as pd
from bs4 import BeautifulSoup

from pyball.utils import read_url, is_savant_url

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SavantScraper:
    """
    A class for scraping baseball statistics from Baseball Savant website.

    Attributes:
    -----------
    url : str
        The URL of the Baseball Savant page to scrape.

    Methods:
    --------
    get_percentile_stats() -> Optional[pd.DataFrame]:
        Returns the (Baseball Savant) percentile stats for a player as a pandas dataframe.

    get_pitching_stats() -> Optional[pd.DataFrame]:
        Returns the (Baseball Savant) pitching stats for a player as a pandas dataframe.

    get_batting_stats() -> Optional[pd.DataFrame]:
        Returns the (Baseball Savant) batting stats for a player as a pandas dataframe.

    get_batted_ball_profile() -> Optional[pd.DataFrame]:
        Returns the (Baseball Savant) batted ball profile for a player as a pandas dataframe.

    get_pitch_tracking() -> Optional[pd.DataFrame]:
        Returns the (Baseball Savant) pitch-specific results for a player as a pandas dataframe.
    """

    TABLE_IDS = {
        "percentile": "percentileRankings",
        "pitching": "statcast_stats_pitching",
        "batting": "statcast_glance_batter",
        "batted_ball": "playeDiscipline",
        "pitch_tracking": "detailedPitches",
    }

    def __init__(self, url: str):
        """
        Initialize the SavantScraper object.

        Parameters:
        -----------
        url : str
            The URL of the Baseball Savant page to scrape.
        """
        if not is_savant_url(url):
            raise ValueError(f"Invalid team URL: {url}")
        self.url = url
        self.soup = self._get_soup()
        if self.soup is None:
            logger.error("Failed to initialize SavantScraper with URL: %s", url)

    def _get_soup(self) -> Optional[BeautifulSoup]:
        """
        Retrieve the BeautifulSoup object for the URL.

        Returns:
        --------
        BeautifulSoup or None
            The BeautifulSoup object representing the HTML content of the URL,
            or None if retrieval failed.
        """
        soup = read_url(self.url)
        if soup is None:
            logger.warning("Failed to retrieve content from URL: %s", self.url)
        return soup

    def _find_table(self, table_id: str) -> Optional[BeautifulSoup]:
        """
        Find the table with the given ID in the HTML content.

        Parameters:
        -----------
        table_id : str
            The ID of the table to find.

        Returns:
        --------
        BeautifulSoup or None
            The BeautifulSoup object representing the table, or None if the table was not found.
        """
        table = self.soup.find("table", id=self.TABLE_IDS[table_id])
        if table is None:
            # Check if the table is inside a div
            div = self.soup.find("div", id=self.TABLE_IDS[table_id])
            if div is not None:
                table = div.find("table")
        if table is None:
            logger.warning(
                "Table with id '%s' not found for URL: %s. Is the player the right position?",
                self.TABLE_IDS[table_id],
                self.url,
            )
        return table

    def _get_dataframe(self, table_id: str) -> Optional[pd.DataFrame]:
        """
        Get the pandas DataFrame for the table with the given ID.

        Parameters:
        -----------
        table_id : str
            The ID of the table to retrieve.

        Returns:
        --------
        pandas.DataFrame or None
            The pandas DataFrame representing the table, or None if the table was not found or parsing failed.
        """
        table = self._find_table(table_id)
        if table is None:
            return None
        try:
            df = pd.read_html(str(table))[0]
            df = df.dropna(how="all")
            return df
        except ValueError as e:
            logger.error(
                "Error parsing %s table (no tables found): %s", table_id, str(e)
            )
            return None
        except Exception as e:
            logger.error("Unexpected error parsing %s table: %s", table_id, str(e))
            return None

    def get_percentile_stats(self) -> Optional[pd.DataFrame]:
        """
        Returns the (Baseball Savant) percentile stats for a player as a pandas dataframe.

        Returns:
        --------
        pandas.DataFrame or None
            Contains the percentile stats for the player, or None if not found.
        """
        return self._get_dataframe("percentile")

    def get_pitching_stats(self) -> Optional[pd.DataFrame]:
        """
        Returns the (Baseball Savant) pitching stats for a player as a pandas dataframe.

        Returns:
        --------
        pandas.DataFrame or None
            Contains the savant pitching stats for the player, or None if not found.
        """
        return self._get_dataframe("pitching")

    def get_batting_stats(self) -> Optional[pd.DataFrame]:
        """
        Returns the (Baseball Savant) batting stats for a player as a pandas dataframe.

        Returns:
        --------
        pandas.DataFrame or None
            Contains the savant batting stats for the player, or None if not found.
        """
        return self._get_dataframe("batting")

    def get_batted_ball_profile(self) -> Optional[pd.DataFrame]:
        """
        Returns the (Baseball Savant) batted ball profile for a player as a pandas dataframe.

        Returns:
        --------
        pandas.DataFrame or None
            Contains the batted ball profile for the player, or None if not found.
        """
        return self._get_dataframe("batted_ball")

    def get_pitch_tracking(self) -> Optional[pd.DataFrame]:
        """
        Returns the (Baseball Savant) pitch-specific results for a player as a pandas dataframe.

        Returns:
        --------
        pandas.DataFrame or None
            Contains the pitch-specific results for the player, or None if not found.
        """
        return self._get_dataframe("pitch_tracking")
