#
# 2011 andrewkittredge
#
# (No License)
#
# https://github.com/andrewkittredge/Baseball-Reference-Scraping
#

#
# modified by gdifiore 2018
#
# translated to python3 & other fixes (include year) & adapted to pitching
#

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
import itertools
from string import ascii_letters
import sys

PLAYERS_PAGE_TEMPLATE='http://www.baseball-reference.com/players/%(letter)s/'

STANDARD_PITCHING_COLUMNS=(
    'Age',
    'Team',
    'League',
    'W',
    'L',
    'Win-Loss Percentage',
    'ERA',
    'G',
    'GS',
    'Games Finished',
    'CG',
    'SHO',
    'SV',
    'IP',
    'H',
    'H',
    'ER',
    'HR',
    'BB',
    'IBB',
    'SO',
    'HBP',
    'BK',
    'WP',
    'BF',
    'ERA+',
    'FIP',
    'WHIP',
    'H9',
    'HR9',
    'BB9',
    'SO9',
    'SO/W',
    'Awards',
    'Year'
)


def find_pitching_standard_table(soup):
    for table in soup.findAll('table'):
        try:
            if table['id'] == 'pitching_standard':
                for tag in soup.select('tr.minors_table'):
                    tag.decompose()
                for tag in soup.select('thead'):
                    tag.decompose()
                return table
        except KeyError:
            #table does not have an "id" attribute, oh-well, the table we're looking for does
            pass
    #exception_string = 'Did not find "pitching_standard" table in %s' % soup
    #raise BaseballReferenceParsingException(exception_string)

pitching_standard_re = 'pitching_standard\.((18|19|20)[0-9]{2})'

def decompose_pitching_table(pitching_table_soup):
    # Takes the soup of pitching statistics table
    stats = []
    pitching_table_body = pitching_table_soup.findAll('tbody')[0]
    for table_row in pitching_table_body.findAll('tr'):
        table_row_id = table_row.get('id')
        if not table_row_id:
            continue
        year = re.findall(pitching_standard_re, table_row_id)
        row_values = {}
        values = [element.text for element in table_row.findAll('td')]
        values_with_years = [element.text for element in table_row.findAll('th')]
        values.extend(values_with_years)
        my_keys_with_values = list(zip(STANDARD_PITCHING_COLUMNS, values))
        row_values = dict(my_keys_with_values)

        stats.append(row_values)
    return stats

def pitching_stats_from_soup(soup):
    pitching_table = find_pitching_standard_table(soup)
    if pitching_table:
        stats = decompose_pitching_table(pitching_table)
        return stats