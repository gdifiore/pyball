#
# File: baseball_reference_team.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# (c) 2022-2024
#
# Description: File containing functions to obtain team stats from Baseball-Reference
#

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
    TEAM_BATTING_TABLE_ID : str
        The HTML id of the table containing team batting statistics on Baseball-Reference.
    TEAM_PITCHING_TABLE_ID : str
        The HTML id of the table containing team pitching statistics on Baseball-Reference.
    """

    TEAM_BATTING_TABLE_ID = "team_batting"
    TEAM_PITCHING_TABLE_ID = "team_pitching"

    @staticmethod
    def _find_team_batting_table(soup: BeautifulSoup) -> Optional[BeautifulSoup]:
        """
        Find the team batting stats table (Baseball-Reference) in the soup.

        Parameters:
        -----------
        soup : BeautifulSoup
            Contains the HTML of the team page.

        Returns:
        --------
        Optional[BeautifulSoup]
            Contains the HTML of the batting stats table, or None if not found.
        """
        return soup.find("table", id=BaseballReferenceTeamStatsScraper.TEAM_BATTING_TABLE_ID)

    @staticmethod
    def team_batting_stats(url: str) -> Optional[pd.DataFrame]:
        """
        Return the (Baseball-Reference) team batting stats for a team as a pandas dataframe.

        Parameters:
        -----------
        url : str
            URL of the team page.

        Returns:
        --------
        Optional[pd.DataFrame]
            Contains the team batting stats, or None if not available.
        """
        if not is_bbref_team_url(url):
            logger.warning("Invalid team URL: %s", url)
            return None

        soup = read_url(url)
        if soup is None:
            logger.warning("Failed to retrieve content from URL: %s", url)
            return None

        table = BaseballReferenceTeamStatsScraper._find_team_batting_table(soup)
        if table is None:
            logger.warning("Team batting stats table not found for URL: %s", url)
            return None

        try:
            df = pd.read_html(str(table))[0]
            return df.dropna(how="all")
        except ValueError as e:
            logger.error("Error parsing team batting stats table (no tables found): %s", str(e))
            return None
        except Exception as e:
            logger.error("Error parsing team batting stats table: %s", str(e))
            return None

    @staticmethod
    def _find_team_pitching_table(soup: BeautifulSoup) -> Optional[BeautifulSoup]:
        """
        Find the team pitching stats table (Baseball-Reference) in the soup.

        Parameters:
        -----------
        soup : BeautifulSoup
            Contains the HTML of the team page.

        Returns:
        --------
        Optional[BeautifulSoup]
            Contains the HTML of the pitching stats table, or None if not found.
        """
        return soup.find("table", id=BaseballReferenceTeamStatsScraper.TEAM_PITCHING_TABLE_ID)

    @staticmethod
    def team_pitching_stats(url: str) -> Optional[pd.DataFrame]:
        """
        Return the (Baseball-Reference) team pitching stats for a team as a pandas dataframe.

        Parameters:
        -----------
        url : str
            URL of the team page.

        Returns:
        --------
        Optional[pd.DataFrame]
            Contains the team pitching stats, or None if not available.
        """
        if not is_bbref_team_url(url):
            logger.warning("Invalid team URL: %s", url)
            return None

        soup = read_url(url)
        if soup is None:
            logger.warning("Failed to retrieve content from URL: %s", url)
            return None

        table = BaseballReferenceTeamStatsScraper._find_team_pitching_table(soup)
        if table is None:
            logger.warning("Team pitching stats table not found for URL: %s", url)
            return None

        try:
            df = pd.read_html(str(table))[0]
            return df.dropna(how="all")
        except ValueError as e:
            logger.error("Error parsing team pitching stats table (no tables found): %s", str(e))
            return None
        except Exception as e:
            logger.error("Error parsing team pitching stats table: %s", str(e))
            return None
