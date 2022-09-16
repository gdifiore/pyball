#
# File: pitching_stats.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# Date: 9/14/2022
#
# Description: File containing functions to obtain player batting data from baseball-reference
#

import pandas as pd

from pyball.utils import readURL

def findPitchingTable(soup):
    """
    Function to find the pitching stats table in the soup

    Parameters
    ----------
    soup: BeautifulSoup object
        Contains the html of the player page

    Returns
    ----------
    BeautifulSoup object
        Contains the html of the pitching stats table
    """
    table = soup.find('table', id='pitching_standard')

    return table

def pitching_stats(url):
    """
    Function to return the pitching stats for a player as a pandas dataframe

    Parameters
    ----------
    url: String
        url of the player page

    Returns
    ----------
    pandas dataframe
        Contains the pitching stats for the player
    """
    soup = readURL(url)
    table = findPitchingTable(soup)

    df = pd.read_html(str(table))[0]

    return df.dropna(how='all')
