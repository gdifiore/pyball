#
# File: utils.py
# Author: Gabriel DiFiore <difioregabe@gmail.com>
# Date: 9/14/2022
#
# Description: File containing various utility functions used in pyball
#

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
import logging
from functools import lru_cache, wraps
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def timed_lru_cache(seconds: int, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

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
    logger.info(f"Fetching new page: {url}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)  # Increased timeout to 60 seconds

            # Specific handling for different sites
            if "baseball-reference.com" in url:
                logger.info("Detected Baseball-Reference page")
                page.wait_for_selector('div#inner_nav', timeout=30000)
            elif "baseballsavant" in url:
                logger.info("Detected Baseball Savant page")
                page.wait_for_selector("div.pitchingBreakdown table#detailedPitches", timeout=30000)

            html = page.content()
            logger.info("Page content retrieved successfully")
        except PlaywrightTimeoutError as e:
            logger.error(f"Timeout error occurred: {str(e)}")
            html = page.content()  # Get whatever content is available
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            html = None
        finally:
            browser.close()

    if html:
        soup = BeautifulSoup(html, "html.parser")
        return soup
    else:
        logger.warning("Failed to retrieve page content")
        return None


def make_bbref_url(bbref_key):
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


def make_savant_url(last, first, key_mlbam):
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


def create_team_url(team, year):
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
