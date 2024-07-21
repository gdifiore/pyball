# File: savant.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# (c) 2022-2024
#
# Description: File containing functions to obtain player savant data

from typing import Optional
import logging
import pandas as pd
from bs4 import BeautifulSoup

from pyball.utils import read_url

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SavantScraper:
    TABLE_IDS = {
        'percentile': 'percentileRankings',
        'pitching': 'statcast_stats_pitching',
        'batting': 'statcast_glance_batter',
        'batted_ball': 'playeDiscipline',
        'pitch_tracking': 'detailedPitches'
    }

    def __init__(self, url: str):
        self.url = url
        self.soup = self._get_soup()
        if self.soup is None:
            logger.error("Failed to initialize SavantScraper with URL: %s", url)

    def _get_soup(self) -> Optional[BeautifulSoup]:
        soup = read_url(self.url)
        if soup is None:
            logger.warning("Failed to retrieve content from URL: %s", self.url)
        return soup

    def _find_table(self, table_id: str) -> Optional[BeautifulSoup]:
        table = self.soup.find("table", id=self.TABLE_IDS[table_id])
        if table is None:
            logger.warning("Table with id '%s' not found for URL: %s", table_id, self.url)
        return table

    def _get_dataframe(self, table_id: str) -> Optional[pd.DataFrame]:
        table = self._find_table(table_id)
        if table is None:
            return None
        try:
            df = pd.read_html(str(table))[0]
            df = df.dropna(how="all")
            if table_id in ['pitching', 'batting'] and not df.empty:
                df = df.drop(df.index[-1])  # drop last row of MLB average
            return df
        except ValueError as e:
            logger.error("Error parsing %s table (no tables found): %s", table_id, str(e))
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
        return self._get_dataframe('percentile')

    def get_pitching_stats(self) -> Optional[pd.DataFrame]:
        """
        Returns the (Baseball Savant) pitching stats for a player as a pandas dataframe.

        Returns:
        --------
        pandas.DataFrame or None
            Contains the savant pitching stats for the player, or None if not found.
        """
        return self._get_dataframe('pitching')

    def get_batting_stats(self) -> Optional[pd.DataFrame]:
        """
        Returns the (Baseball Savant) batting stats for a player as a pandas dataframe.

        Returns:
        --------
        pandas.DataFrame or None
            Contains the savant batting stats for the player, or None if not found.
        """
        return self._get_dataframe('batting')

    def get_batted_ball_profile(self) -> Optional[pd.DataFrame]:
        """
        Returns the (Baseball Savant) batted ball profile for a player as a pandas dataframe.

        Returns:
        --------
        pandas.DataFrame or None
            Contains the batted ball profile for the player, or None if not found.
        """
        return self._get_dataframe('batted_ball')

    def get_pitch_tracking(self) -> Optional[pd.DataFrame]:
        """
        Returns the (Baseball Savant) pitch-specific results for a player as a pandas dataframe.

        Returns:
        --------
        pandas.DataFrame or None
            Contains the pitch-specific results for the player, or None if not found.
        """
        return self._get_dataframe('pitch_tracking')
