# File: utils.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# Date: 9/14/2022
#
# Description: File containing various utility functions used in pyball

from functools import lru_cache, wraps
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup


def timed_lru_cache(seconds: int, maxsize: int = 128):
    """
    A decorator that combines LRU caching with a time-based expiration.

    Args:
        seconds (int): The number of seconds after which the cache should expire.
        maxsize (int, optional): The maximum number of function calls to cache. Defaults to 128.

    Returns:
        function: The decorated function.
    """
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.now() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.now() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.now() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


@timed_lru_cache(seconds=86400)  # Cache for 1 day
def read_url(url):
    """
    Function to read a url and return the html content using Playwright

    Parameters
    ----------
    url: String
        url to read

    Returns
    ----------
    BeautifulSoup object
        Contains the html of the url
    """
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
        soup = BeautifulSoup(html, "html.parser")
        return soup
    else:
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
        bool: True if the URL contains 'players', False otherwise.
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
        bool: True if the URL contains 'teams', False otherwise.
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
