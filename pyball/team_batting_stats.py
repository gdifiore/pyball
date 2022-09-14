#
# File: team_batting_stats.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# Date: 9/14/2022
#
# Description: File containing functions to obtain team batting data from baseball-reference
#

import pandas as pd

from pyball.utils import readURL

def findTeamBattingTable(soup):
    """Function to find the team batting stats table in the soup"""
    table = soup.find('table', id='team_batting')

    return table

def team_batting_stats(url):
    """Function to return the team batting stats for a team as a pandas dataframe"""
    soup = readURL(url)
    table = findTeamBattingTable(soup)

    df = pd.read_html(str(table))[0]

    return df.dropna(how='all')
