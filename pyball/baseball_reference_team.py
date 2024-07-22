# File: baseball_reference_team.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# (c) 2022-2024
#
# Description: File containing functions to obtain team stats from Baseball-Reference

from typing import Optional
import logging
import pandas as pd
from bs4 import BeautifulSoup

from pyball.utils import read_url, is_bbref_team_url

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseballReferenceTeamStatsScraper:
    """
    A class for scraping team statistics from Baseball-Reference.

    This class provides methods to extract batting and pitching statistics
    for baseball teams from their Baseball-Reference pages.

    Attributes:
    -----------
    url : str
        The URL of the Baseball-Reference page for the team.

    Methods:
    --------
    batting_stats(self) -> Optional[pd.DataFrame]
        Returns the batting stats for the team as a pandas DataFrame.

    pitching_stats(self) -> Optional[pd.DataFrame]
        Returns the pitching stats for the team as a pandas DataFrame.
    """

    TABLE_IDS = {
        'batting': 'team_batting',
        'pitching': 'team_pitching'
    }

    def __init__(self, url: str):
        """
        Initializes a BaseballReferenceTeamStatsScraper instance.

        Parameters:
        -----------
        url : str
            The URL of the Baseball-Reference page for the team.

        Raises:
        -------
        ValueError
            If the provided URL is not a valid Baseball-Reference team URL.
        """
        if not is_bbref_team_url(url):
            raise ValueError(f"Invalid team URL: {url}")
        self.url = url
        self.soup = self._get_soup()

    def _get_soup(self) -> Optional[BeautifulSoup]:
        """
        Retrieves the BeautifulSoup object for the team's Baseball-Reference page.

        Returns:
        --------
        Optional[BeautifulSoup]
            The BeautifulSoup object representing the HTML content of the page,
            or None if the content retrieval fails.
        """
        soup = read_url(self.url)
        if soup is None:
            logger.warning("Failed to retrieve content from URL: %s", self.url)
        return soup

    def _find_table(self, table_id: str) -> Optional[BeautifulSoup]:
        """
        Finds the HTML table element with the specified ID in the team's page.

        Parameters:
        -----------
        table_id : str
            The ID of the table to find.

        Returns:
        --------
        Optional[BeautifulSoup]
            The BeautifulSoup object representing the found table element,
            or None if the table is not found.
        """
        return self.soup.find("table", id=self.TABLE_IDS[table_id])

    def _get_dataframe(self, table_id: str) -> Optional[pd.DataFrame]:
        """
        Parses the HTML table with the specified ID and returns it as a pandas DataFrame.

        Parameters:
        -----------
        table_id : str
            The ID of the table to parse.

        Returns:
        --------
        Optional[pd.DataFrame]
            The parsed table as a pandas DataFrame,
            or None if the table is not found or an error occurs during parsing.
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
        Returns the batting stats for the team as a pandas DataFrame.

        Returns:
        --------
        Optional[pd.DataFrame]
            The batting stats for the team, or None if not available.
        """
        return self._get_dataframe('batting')

    def pitching_stats(self) -> Optional[pd.DataFrame]:
        """
        Returns the pitching stats for the team as a pandas DataFrame.

        Returns:
        --------
        Optional[pd.DataFrame]
            The pitching stats for the team, or None if not available.
        """
        return self._get_dataframe('pitching')
