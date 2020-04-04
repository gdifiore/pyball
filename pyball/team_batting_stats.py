#
# team_batting_stats.py - pyball
#
# (c) 2019-2020 gdifiore <difioregabe@gmail.com>
#

from bs4 import BeautifulSoup
import pandas as pd

def get_team_batting_stats(soup, modifier):
    table = soup.find(id='team_batting')
    n_columns = 0
    n_rows=0
    column_names = []

    # Find number of rows and columns
    # we also find the column titles if we can
    for row in table.find_all('tr'):

        # Determine the number of rows in the table
        td_tags = row.find_all('td')
        if len(td_tags) > 0:
            n_rows+=1
            if n_columns == 0:
                # Set the number of columns for our table
                n_columns = len(td_tags)

        # Handle column names if we find them
        th_tags = row.find_all('th')
        if len(th_tags) > 0 and len(column_names) == 0:
            for th in th_tags:
                column_names.append(th.get_text())
    del column_names[0]

    # Safeguard on Column Titles
    if len(column_names) > 0 and len(column_names) != n_columns:
        raise Exception("Column titles do not match the number of columns")

    columns = column_names if len(column_names) > 0 else range(0,n_columns)
    df = pd.DataFrame(columns = columns, index= range(0,n_rows))
    row_marker = 0
    for row in table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        for column in columns:
            df.iat[row_marker,column_marker] = column.get_text()
            column_marker += 1
        if len(columns) > 0:
            row_marker += 1
    if modifier is 'all':
        return df
    if modifier is 'teamTotal':
        return df[54:-3]
    if modifier is 'positionPlayers':
        return df[:-36]
    if modifier is 'positionPlayersTotal':
        return df[56:-1]
    if modifier is 'pitchers':
        return df[22:-4]
    if modifier is 'pitcherTotals':
        return df[57:]
    if modifier is 'rank':
        return df[55:-2]