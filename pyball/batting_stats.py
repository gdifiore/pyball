#
# File: batting_stats.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# (c) 2022-2024
#
# Description: File containing functions to obtain player batting data from baseball-reference
#

import pandas as pd

from pyball.utils import read_url, is_player_url


def _find_batting_table(soup):
    """
    Function to find the batting stats table (Baseball-Reference) in the soup

    Parameters
    ----------
    soup: BeautifulSoup object
        Contains the html of the player page

    Returns
    ----------
    BeautifulSoup object
        Contains the html of the batting stats table
    """
    table = soup.find("table", id="batting_standard")

    return table


def batting_stats(url):
    """
    Function to return the (Baseball-Reference) batting stats for a player as a pandas dataframe

    Parameters
    ----------
    url: String
        url of the player page

    Returns
    ----------
    pandas dataframe
        Contains the batting stats for the player
    """
    if not is_player_url(url):
        return None

    soup = read_url(url)
    table = _find_batting_table(soup)

    df = pd.read_html(str(table))[0]

    return df.dropna(how="all")
