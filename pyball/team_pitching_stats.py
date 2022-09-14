#
# (c) gdifiore 2022 - difioregabe@gmail.com
#
# File containing functions to obtain team pitching data from baseball-reference
#

import pandas as pd

from pyball.utils import readURL

def findTeamPitchingTable(soup):
    table = soup.find('table', id='team_pitching')

    return table

def team_batting_stats(url):
    """This function returns the pitching stats for a team"""
    soup = readURL(url)
    table = findTeamPitchingTable(soup)

    df = pd.read_html(str(table))[0]

    return df.dropna(how='all')
