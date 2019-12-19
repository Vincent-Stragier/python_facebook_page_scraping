"""
    This module aims to provide a way to scrap posts on a Facebook page, 
    to remove or add emoji and to get the number of likes on a page.
    
    Requirement:
    python3 -m pip install pillow facebook_scraper, demoji, emoji
"""
import requests

# https://pypi.org/project/demoji/
import demoji
from contextlib import redirect_stdout
import io

import emoji

# https://pypi.org/project/facebook-scraper/
from facebook_scraper import get_posts

# Get the number of likes on the Facebook page (using the name of the page)
def getLikeCount(page_name):
    """
    URL = "https://fr-fr.facebook.com/pg/" + PAGE_NAME + "/community/?ref=page_internal"

    LOWER_DELIMITER_0 = "Total des mentions J’aime</div>"
    LOWER_DELIMITER_1 = "</div>"
    UPPER_DELIMITER_0 = "\">"
    
    r = requests.get(URL)
    page_text = r.text
    page_text = page_text[:page_text.find(LOWER_DELIMITER_0)]
    page_text = page_text[:page_text.rfind(LOWER_DELIMITER_1)]
    page_text = page_text[page_text.rfind(UPPER_DELIMITER_0) + len(UPPER_DELIMITER_0):]
    """
    # <div>636&nbsp;124 personnes aiment ça</div>
    URL =  "https://fr-fr.facebook.com/pg/" + page_name
    LOWER_DELIMITER_0 = " personnes aiment ça</div>"
    UPPER_DELIMITER_0 = "<div>"
    SPACE = b'\xc2\xa0'.decode('UTF-8') # Remove space

    r = requests.get(URL)
    page_text = r.text
    page_text = page_text[:page_text.rfind(LOWER_DELIMITER_0)]
    page_text = page_text[page_text.rfind(UPPER_DELIMITER_0) + len(UPPER_DELIMITER_0):].replace(SPACE,'').replace(' ','')
    return page_text if page_text==str(int(page_text)) else "Error: check page name"

# Remove the emoji from the 'data' string
def remove_emoji(data):
    f = io.StringIO()
    with redirect_stdout(f):    # Hide demoji stdout (stored in f.getvalue())
        demoji.download_codes() # Update emoji list

    return demoji.replace(data)

# Return the UTF-8 encoded emoji value
def add_emoji(emoji_name):
    return emoji.emojize(emoji_name)

# Get the first post on the 'page_name' Facebook Page containing the 'key'
def getPost(page_name, key, enable_emoji=True):
    for post in get_posts(page_name):
        if key in post['text'][:]: # Looking for the clock emoji
            if enable_emoji:
                return post['text'][:]
            else:
                return remove_emoji(post['text'][:])
    return None

def main():
    # PAGE_NAME = "electroLAB.FPMs"
    # PAGE_NAME = "codobot.be"
    # PAGE_NAME = "tamu"
    # PAGE_NAME = "UniversiteMons"
    # print(getLikeCount(page_name=PAGE_NAME))
    print("This Python script is a module which can be used to scrap information from a Facebook page.")

if __name__ == "__main__":
    main()