# File: utils.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# Date: 9/14/2022
#
# Description: File containing various utility functions used in pyball

import time
import hashlib
import diskcache
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

cache = diskcache.Cache('./.pyball_cache')



def fetch_url_content(url, cache_time=86400):
    """
    Function to read a URL and return the BeautifulSoup object, using disk cache when available
    """
    # Create a unique key for this URL
    url_hash = hashlib.md5(url.encode()).hexdigest()

    # Check if we have a valid cached version
    cached_data = cache.get(url_hash)
    if cached_data is not None:
        timestamp, html = cached_data
        if time.time() - timestamp < cache_time:
            print("Using cached data")
            return BeautifulSoup(html, "html.parser")

    # If no valid cache, fetch the content
    print("Fetching from URL")
    options = Options()
    options.add_argument("--headless")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)

        # Specific handling for different sites
        if "baseball-reference.com" in url:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#inner_nav')))
        elif "baseballsavant" in url:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.pitchingBreakdown table#detailedPitches")))
        else:
            # Default wait for network idle
            time.sleep(10)  # Simple wait as Selenium doesn't have a built-in "networkidle" equivalent

        html = driver.page_source
    except TimeoutException:
        html = driver.page_source
    finally:
        driver.quit()

    if html:
        # Cache the new content
        cache[url_hash] = (time.time(), html)
        return BeautifulSoup(html, "html.parser")
    else:
        return None

def read_url(url):
    """
    Function to read a URL, using cache when available
    """
    try:
        return fetch_url_content(url)
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None

def make_bbref_player_url(bbref_key):
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


def is_bbref_player_url(url):
    """
    Check if the given URL contains the word 'players'.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL contains 'players' and 'baseball-reference', False otherwise.
    """
    return "players" in url and "baseball-reference" in url


def create_bbref_team_url(team, year):
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


def is_bbref_team_url(url):
    """
    Check if the given URL contains the word 'teams'.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL contains 'teams' and 'baseball-reference', False otherwise.
    """
    return "teams" in url and "baseball-reference" in url


def make_savant_player_url(last, first, key_mlbam):
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
    url = base_url + first + "-" + last + "-" + key_mlbam

    return url


def is_savant_url(url):
    """
    Checks if the given string is a valid Baseball Savant url.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL contains 'baseballsavant', False otherwise.
    """
    return "baseballsavant" in url
