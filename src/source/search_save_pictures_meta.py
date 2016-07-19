"""A Script to make a search request from Flickr API and save data to CSV."""
import shutil
import pandas as pd
import numpy as np
from flickr_api import get_flickr_keys, search_flicker
import sys


if __name__ == '__main__':
    search_tag_term = 'Search Tag is entered incorrectly.'
    search_tag_term = sys.argv[1]
    if len(sys.argv) >= 3:
        max_pages_to_download = int(sys.argv[2])
    flickr_keys = get_flickr_keys('flickr.keys')

    search_kwds = {'method': 'flickr.photos.search',
                   'api_key': flickr_keys['Key'],
                   'sort': 'relavance',
                   'content_type': '1',
                   'per_page': '500',
                   'extras': 'license, date_upload, date_taken, owner_name,\
                              original_format, last_update, geo, tags,\
                              machine_tags, o_dims, views, media, path_alias,\
                              url_o'
                   }

    print ""
    print "Begin Flickr Image Search For {}:".format(search_tag_term.upper())
    picture_soup_data = search_flicker(search_tag_term, search_kwds, max_pages_to_download)