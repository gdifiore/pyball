#
# File: team_pitching_stats.py
# Author: Gabriel DiFiore <difioregabe@gmail.com> & James LeDoux
# Date: 9/14/2022
#
# Description: File containing functions to obtain team pitching data from baseball-reference
#


import pandas as pd

from pyball.utils import readURL

def findTeamPitchingTable(soup):
    """
    Function to find the team pitching stats table (Baseball-Reference) in the soup

    Parameters
    ----------
    soup: BeautifulSoup object
        Contains the html of the team page

    Returns
    ----------
    BeautifulSoup object
        Contains the html of the pitching stats table
    """
    table = soup.find('table', id='team_pitching')

    return table

def team_batting_stats(url):
    """
    Function to return the (Baseball-Reference) team batting stats for a team as a pandas dataframe

    Parameters
    ----------
    url: String
        url of the team page

    Returns
    ----------
    pandas dataframe
        containing the team batting stats for the team
    """
    soup = readURL(url)
    table = findTeamPitchingTable(soup)

    df = pd.read_html(str(table))[0]

    return df.dropna(how='all')
