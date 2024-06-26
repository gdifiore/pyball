#
# File: team_pitching_stats.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# (c) 2022-2024
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
    table = soup.find("table", id="team_pitching")

    return table


def team_pitching_stats(url):
    """
    Function to return the (Baseball-Reference) team pitching stats for a team as a pandas dataframe

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

    return df.dropna(how="all")
