#
# File: savant.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# (c) 2022-2024
#
# Description: File containing functions to obtain player savant data
#

import pandas as pd

from pyball.utils import read_url


def _find_percentiles_table(soup):
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
    table = soup.find("table", id="percentileRankings")

    return table


def savant_percentile_stats(url):
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
    soup = read_url(url)
    table = _find_percentiles_table(soup)

    df = pd.read_html(str(table))[0]

    return df.dropna(how="all")


def _find_statcast_pitching_stats_table(soup):
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
    div = soup.find("div", id="statcast_stats_pitching")
    if div is None:
        print("Not a pitcher page")
        return None
    # get table inside div
    table = div.find("table")

    return table


def savant_pitching_statcast_stats(url):
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
    soup = read_url(url)
    table = _find_statcast_pitching_stats_table(soup)

    if table is None:
        return None

    df = pd.read_html(str(table))[0]

    # drop a row of all NA and drop last row of MLB average
    return df.dropna(how="all").drop(df.index[-1])


def _find_statcast_batting_stats_table(soup):
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
    div = soup.find("div", id="statcast_glance_batter")
    if div is None:
        print("Not a pitcher page")
        return None

    table = div.find("table")

    return table


def savant_batting_statcast_stats(url):
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
    soup = read_url(url)
    table = _find_statcast_batting_stats_table(soup)

    if table is None:
        return None

    df = pd.read_html(str(table))[0]

    # drop a row of all NA and drop last row of MLB average
    return df.dropna(how="all").drop(df.index[-1])


def _find_batted_ball_profile_table(soup):
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
    table = soup.find("table", id="playeDiscipline")

    return table


def savant_batted_ball_profile(url):
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
    soup = read_url(url)
    table = _find_batted_ball_profile_table(soup)

    df = pd.read_html(str(table))[0]

    return df.dropna(how="all")


def _find_pitch_tracking_table(soup):
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
    table = soup.find("table", id="detailedPitches")

    return table


def savant_pitch_tracking(url):
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
    soup = read_url(url)
    table = _find_pitch_tracking_table(soup)

    df = pd.read_html(str(table))[0]

    return df.dropna(how="all")
