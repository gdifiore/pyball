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
    """Function to find the savant stat percentiles table in the soup"""
    table = soup.find('table', id='percentileRankings')

    return table

def savantPercentileStats(url):
    """Function to return the percentile stats for a player as a pandas dataframe"""
    soup = readURL(url)
    table = findPercentilesTable(soup)

    df = pd.read_html(str(table))[0]

    return df.dropna(how='all')

def findStatcastPitchingStatsTable(soup):
    """Function to find the statcast pitching stats table in the soup"""
    div = soup.find('div', id='statcast_stats_pitching')
    # get table inside div
    table = div.find('table')

    return table

def savantPitchingStatcastStats(url):
    """Function to return the savant pitching stats for a player as a pandas dataframe"""
    soup = readURL(url)
    table = findStatcastPitchingStatsTable(soup)

    df = pd.read_html(str(table))[0]

    # drop a row of all NA and drop last row of MLB average
    return df.dropna(how='all').drop(df.index[-1])

def findStatcastBattingStatsTable(soup):
    """Function to find the statcast batting stats table in the soup"""
    # Find div with id 'statcast_glance_batter' and get table inside
    div = soup.find('div', id='statcast_glance_batter')
    table = div.find('table')

    return table

def savantBattingStatcastStats(url):
    """Function to return the savant batting stats for a player as a pandas dataframe"""
    soup = readURL(url)
    table = findStatcastBattingStatsTable(soup)

    df = pd.read_html(str(table))[0]

    # drop a row of all NA and drop last row of MLB average
    return df.dropna(how='all').drop(df.index[-1])

def findBattedBallProfileTable(soup):
    """Function to find the batted ball profile table in the soup"""
    table = soup.find('table', id='playeDiscipline')

    return table

def savantBattedBallProfile(url):
    """Function to return the batted ball profile for a player as a pandas dataframe"""
    soup = readURL(url)
    table = findBattedBallProfileTable(soup)

    df = pd.read_html(str(table))[0]

    return df.dropna(how='all')

def findPitchTrackingTable(soup):
    """Function to find the pitch tracking table in the soup"""
    table = soup.find('table', id='detailedPitches')

    return table

def savantPitchTracking(url):
    """Function returns the pitch-specific results for a player as a pandas dataframe"""
    soup = readURL(url)
    table = findPitchTrackingTable(soup)

    df = pd.read_html(str(table))[0]

    return df.dropna(how='all')