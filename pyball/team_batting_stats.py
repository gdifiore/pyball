#
# (c) gdifiore 2022 - difioregabe@gmail.com
#
# File containing functions to obtain team batting data from baseball-reference
#

import pandas as pd

from pyball.utils import readURL

def findTeamBattingTable(soup):
    table = soup.find('table', id='team_batting')

    return table

def team_batting_stats(url):
    """This function returns the batting stats for a team"""
    soup = readURL(url)
    table = findTeamBattingTable(soup)

    df = pd.read_html(str(table))[0]

    return df.dropna(how='all')
