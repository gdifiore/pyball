#
# File: batting_stats.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# Date: 9/14/2022
#
# Description: File containing functions to obtain player batting data from baseball-reference
#

import pandas as pd

from pyball.utils import readURL

def findBattingTable(soup):
    """Functio to find the batting stats table in the soup"""
    table = soup.find('table', id='batting_standard')

    return table

def batting_stats(url):
    """Function to return the batting stats for a player as a pandas dataframe"""
    soup = readURL(url)
    table = findBattingTable(soup)

    df = pd.read_html(str(table))[0]

    return df.dropna(how='all')
