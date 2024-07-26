# File: utils.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# Date: 9/14/2022
#
# Description: File containing various utility functions used in pyball

import time
import hashlib
import diskcache
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


cache = diskcache.Cache('./.pyball_cache')


def fetch_url_content(url, cache_time=86400):
    """
    Function to read a url and return the BeautifulSoup object, using disk cache when available
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
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        html = None
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)

            # Specific handling for different sites
            if "baseball-reference.com" in url:
                page.wait_for_selector('div#inner_nav', timeout=30000)
            elif "baseballsavant" in url:
                page.wait_for_selector("div.pitchingBreakdown table#detailedPitches", timeout=30000)

            html = page.content()
        except PlaywrightTimeoutError:
            html = page.content()
        finally:
            browser.close()

    if html:
        # Cache the new content
        cache.set(url_hash, (time.time(), html))
        return BeautifulSoup(html, "html.parser")
    else:
        return None


def read_url(url):
    """
    Function to read a url, using cache when available
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
