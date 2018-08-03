#
# utils.py - pyball
#
# (c) 2018 gdifiore <difioregabe@gmail.com>
#

def makeURL(bbref_key):
    base_url = "https://www.baseball-reference.com/players/"
    url = base_url + bbref_key[0] + "/" + bbref_key + ".shtml"

    return url

def toValidJSON(json_string):
    validJSON = json_string.replace("'", '"')

    return validJSON