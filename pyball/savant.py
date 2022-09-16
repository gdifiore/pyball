#
# File: savant.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# Date: 9/14/2022
#
# Description: File containing functions to obtain player savant data
#

import pandas as pd

from pyball.utils import readURL

def findPercentilesTable(soup):
    """
    Function to find the stat percentiles table (Baseball Savant) in the soup

    Parameters
    ----------
    soup : BeautifulSoup object
        Contains the html of the player page

    Returns
    -------
    BeautifulSoup object
        Contains the html of the savant stat percentiles table
    """
    table = soup.find('table', id='percentileRankings')

    return table

def savantPercentileStats(url):
    """
    Function to return the (Baseball Savant) percentile stats for a player as a pandas dataframe

    Parameters
    ----------
    url : String
        url of the player page

    Returns
    ----------
    pandas dataframe
        Contains the percentile stats for the player
    """
    soup = readURL(url)
    table = findPercentilesTable(soup)

    df = pd.read_html(str(table))[0]

    return df.dropna(how='all')

def findStatcastPitchingStatsTable(soup):
    """
    Function to find the statcast pitching stats table (Baseball Savant) in the soup

    Parameters
    ----------
    soup : BeautifulSoup object
        Contains the html of the player page

    Returns
    ----------
    BeautifulSoup object
        Contains the html of the statcast pitching stats table
    """
    div = soup.find('div', id='statcast_stats_pitching')
    # get table inside div
    table = div.find('table')

    return table

def savantPitchingStatcastStats(url):
    """
    Function to return the (Baseball Savant) pitching stats for a player as a pandas dataframe

    Parameters
    ----------
    url : String
        url of the player page

    Returns
    ----------
    pandas dataframe
        Contains the savant pitching stats for the player
    """
    soup = readURL(url)
    table = findStatcastPitchingStatsTable(soup)

    df = pd.read_html(str(table))[0]

    # drop a row of all NA and drop last row of MLB average
    return df.dropna(how='all').drop(df.index[-1])

def findStatcastBattingStatsTable(soup):
    """
    Function to find the statcast batting stats table (Baseball Savant) in the soup

    Parameters
    ----------
    soup : BeautifulSoup object
        Contains the html of the player page

    Returns
    ----------
    BeautifulSoup object
        Contains the html of the statcast batting stats table
    """
    # Find div with id 'statcast_glance_batter' and get table inside
    div = soup.find('div', id='statcast_glance_batter')
    table = div.find('table')

    return table

def savantBattingStatcastStats(url):
    """
    Function to return the (Baseball Savant) batting stats for a player as a pandas dataframe

    Parameters
    ----------
    url : String
        url of the player page

    Returns
    ----------
    pandas dataframe
        Contains the savant batting stats for the player
    """
    soup = readURL(url)
    table = findStatcastBattingStatsTable(soup)

    df = pd.read_html(str(table))[0]

    # drop a row of all NA and drop last row of MLB average
    return df.dropna(how='all').drop(df.index[-1])

def findBattedBallProfileTable(soup):
    """
    Function to find the batted ball profile table (Baseball Savant) in the soup

    Parameters
    ----------
    soup : BeautifulSoup object
        Contains the html of the player page

    Returns
    ----------
    BeautifulSoup object
        Contains the html of the batted ball profile table
    """
    table = soup.find('table', id='playeDiscipline')

    return table

def savantBattedBallProfile(url):
    """
    Function to return the (Baseball Savant) batted ball profile for a player as a pandas dataframe

    Parameters
    ----------
    url : String
        url of the player page

    Returns
    ----------
    pandas dataframe
        Contains the batted ball profile for the player
    """
    soup = readURL(url)
    table = findBattedBallProfileTable(soup)

    df = pd.read_html(str(table))[0]

    return df.dropna(how='all')

def findPitchTrackingTable(soup):
    """
    Function to find the pitch tracking table (Baseball Savant) in the soup

    Parameters
    ----------
    soup : BeautifulSoup object
        Contains the html of the player page

    Returns
    ----------
    BeautifulSoup object
        Contains the html of the pitch tracking table
    """
    table = soup.find('table', id='detailedPitches')

    return table

def savantPitchTracking(url):
    """
    Function returns the (Baseball Savant) pitch-specific results for a player as a pandas dataframe

    Parameters
    ----------
    url : String
        url of the player page

    Returns
    ----------
    pandas dataframe
        Contains the pitch-specific results for the player
    """
    soup = readURL(url)
    table = findPitchTrackingTable(soup)

    df = pd.read_html(str(table))[0]

    return df.dropna(how='all')