#
# (c) gdifiore 2022 - difioregabe@gmail.com
#
# File containing functions to obtain player batting data from baseball-reference
#

import pandas as pd

from pyball.utils import readURL

def findPitchingTable(soup):
    table = soup.find('table', id='pitching_standard')

    return table

def pitching_stats(url):
    """This function returns the pitching stats for a player"""
    soup = readURL(url)
    table = findPitchingTable(soup)

    df = pd.read_html(str(table))[0]

    return df.dropna(how='all')
