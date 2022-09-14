#
# (c) gdifiore 2022 - difioregabe@gmail.com
#
# File containing functions to obtain player batting data from baseball-reference
#

import pandas as pd

from pyball.utils import readURL

def findBattingTable(soup):
    table = soup.find('table', id='batting_standard')

    return table

def batting_stats(url):
    """This function returns the batting stats for a player"""
    soup = readURL(url)
    table = findBattingTable(soup)

    df = pd.read_html(str(table))[0]

    return df.dropna(how='all')
