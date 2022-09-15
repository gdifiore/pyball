#
# Copyright (c) 2017 James LeDoux
#
# (Under MIT License)
#
# https://github.com/jldbc/pybaseball
#

#
# File: playerid_lookup.py
# Author: Gabriel DiFiore <difioregabe@gmail.com> & James LeDoux
# Date: 9/14/2022
#
# Description: File containing functions to obtain player (id) information from a lookup table
#              Modified to only gets name, baseball-reference/mlbam key and years played
#

import pandas as pd
import requests
import io

def get_lookup_table():
    """
    Function to download a lookup table of all players

    @return pandas dataframe containing the lookup table
    """
    print('Gathering player lookup table. This may take a moment.')
    url = "https://raw.githubusercontent.com/chadwickbureau/register/master/data/people.csv"
    s = requests.get(url).content
    table = pd.read_csv(io.StringIO(s.decode('utf-8')), dtype={'key_sr_nfl': object, 'key_sr_nba': object, 'key_sr_nhl': object})
    #subset columns
    cols_to_keep = ['name_last','name_first', 'key_bbref', 'key_mlbam', 'mlb_played_first','mlb_played_last']
    table = table[cols_to_keep]
    #make these lowercase to avoid capitalization mistakes when searching
    table['name_last'] = table['name_last'].str.lower()
    table['name_first'] = table['name_first'].str.lower()
    return table


def playerid_lookup(last, first=None):
    """
    Function to lookup a player's baseball reference and mlbam id given their name, from the lookup table

    @param last: last name of the player
    @param first: first name of the player

    @return: pandas dataframe containing the player's name, baseball-reference id, mlbam id, and years played
    """
    # force input strings to lowercase
    last = last.lower()

    if first:
        first = first.lower()

    table = get_lookup_table()

    if first is None:
        results = table.loc[table['name_last']==last]
    else:
        results = table.loc[(table['name_last']==last) & (table['name_first']==first)]

    results = results.reset_index().drop('index', 1)

    return results