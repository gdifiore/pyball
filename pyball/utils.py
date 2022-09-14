#
# utils.py - pyball
#
# (c) 2022 gdifiore <difioregabe@gmail.com>
#

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()

def readURL(url):
    # Theres one or two dynamic tables on baseball savant that are dynamic based on javascript, which requests cannot handle
    # so we use selenium to get the page source and then use beautiful soup to parse it
    # Follow this tutorial to install selenium and chromedriver: https://medium.com/@soumyadip_95708/web-scraping-using-selenium-and-beautifulsoup-6b2a3f7c7c5a
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    html = driver.page_source
    driver.close()

    soup = BeautifulSoup(html, 'html.parser')

    return soup

def makeBBRefURL(bbref_key):
    base_url = "https://www.baseball-reference.com/players/"
    url = base_url + bbref_key[0] + "/" + bbref_key + ".shtml"

    return url

def makeSavantURL(last, first, key_mlbam):
    base_url = "https://baseballsavant.mlb.com/savant-player/"
    url = base_url + last + "-" + first + "-" + key_mlbam

    return url

def toValidJSON(json_string):
    validJSON = json_string.replace("'", '"')

    return validJSON

def createTeamURL(team, year):
    base_url = "https://www.baseball-reference.com/teams/"
    url = base_url + team + "/" + year + ".shtml"

    return url