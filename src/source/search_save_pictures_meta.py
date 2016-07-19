"""A Script to make a search request from Flickr API and save data to CSV."""
import shutil
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from src.source.flickr_api import get_flickr_keys
import sys


def search_flicker(search_tag_term, search_kwds):
    """Search Flicker API for photos including a tagged term."""
    soup, status = flickr_search_results_page(search_tag_term, 1, search_kwds)
    total_pages = int(soup.photos.get('pages'))
    return None


def flickr_search_results_page(search_tag_term, page_num, search_kwds):
    """Return a single API photo search results page."""
    search_url = 'https://api.flickr.com/services/rest/'
    search_kwds['page'] = page_num
    search_kwds['tags'] = search_tag_term

    r = requests.get(search_url, params=search_kwds)
    soup = BeautifulSoup(r.text, 'lxml')

    return soup, r.status_code

if __name__ == '__main__':
    search_tag_term = sys.argv[0]
    flickr_keys = get_flickr_keys('flickr.keys')

    search_kwds = {'method': 'flickr.photos.search',
                   'api_key': flickr_keys['Key'],
                   'sort': 'relavance',
                   'content_type': '1',
                   'per_page': '500',
                   'extras': 'license, date_upload, date_taken, owner_name, original_format, last_update, geo, tags, machine_tags, o_dims, views, media, path_alias, url_o'
                   }

    search_flicker(search_tag_term, search_kwds)
    # Run Initial Request to Test Search Term


    # Continue with Remaining Pages
