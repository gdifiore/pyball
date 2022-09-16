#
# File: utils.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# Date: 9/14/2022
#
# Description: File containing various utility functions used in pyball
#

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
cache = dict()

def readURL(url):
    """
    Function to read a url and return the html content

    Parameters
    ----------
    url: String
        url to read

    Returns
    ----------
    BeautifulSoup object
        Contains the html of the url
    """
    if url not in cache:
        # Theres one or two dynamic tables on baseball savant that are dynamic based on javascript, which requests cannot handle
        # so we use selenium to get the page source and then use beautiful soup to parse it
        # Follow this tutorial to install selenium and chromedriver: https://medium.com/@soumyadip_95708/web-scraping-using-selenium-and-beautifulsoup-6b2a3f7c7c5a
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)
        # wait for the page to fully load
        if "baseballsavant" in url:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "detailedPitches"))
            )
        html = driver.page_source
        driver.close()

        soup = BeautifulSoup(html, 'html.parser')
        cache[url] = soup
    else:
        soup = cache[url]

    return soup

def makeBBRefURL(bbref_key):
    """
    Function to generate baseball-reference url from bbref_key

    Parameters
    ----------
    bref_key: String
        bbref_key of the player

    Returns
    ----------
    String
        baseball-reference url of the player
    """
    base_url = "https://www.baseball-reference.com/players/"
    url = base_url + bbref_key[0] + "/" + bbref_key + ".shtml"

    return url

def makeSavantURL(last, first, key_mlbam):
    """
    Function to generate baseball savant url from last name, first name, and mlbam key

    Parameters
    ----------
    last: String
        last name of the player
    first: String
        first name of the player
    key_mlbam: String
        mlbam key of the player

    Returns
    ----------
    String
        baseball savant url of the player
    """
    base_url = "https://baseballsavant.mlb.com/savant-player/"
    url = base_url + last + "-" + first + "-" + key_mlbam

    return url

def createTeamURL(team, year):
    """
    Function to create a baseball-reference team url from team and year

    Parameters
    ----------
    team: String
        team name

    Returns
    ----------
    String
        baseball-reference team url
    """
    base_url = "https://www.baseball-reference.com/teams/"
    url = base_url + team + "/" + year + ".shtml"

    return url