"""Saved methods for Flickr API use."""
import requests
from bs4 import BeautifulSoup
import sys


def get_flickr_keys(filename='flickr.keys'):
    """Get the Ficker user and app keys from the .keys file."""
    keys_list = []
    flickr_keys = {}
    with open(filename) as f_open:
        for line in f_open:
            keys_list.append(line.strip('\n'))
    for key in keys_list:
        pair = key.split(":")
        flickr_keys[pair[0]] = pair[1]
    return flickr_keys


def search_flicker(search_tag_term, search_kwds, max_pages_to_download=None):
    """Search Flicker API for photos including a tagged term."""
    picture_soup_data = []
    search_kwds['tags'] = search_tag_term

    # Run a first pass to test results.
    soup, status = flickr_search_results_page(search_tag_term, 1, search_kwds)
    if int(status) == 200:
        picture_soup_data.extend(soup.findAll('photo'))
        total_pages = int(soup.photos.get('pages'))
        print "Search Results:  {} Pages Found".format(total_pages)
    else:
        print "Error: \tStatus Code {}".format(status)
        return None

    if max_pages_to_download is not None:
        print "Downloading First {} Pages of Results".format(
                                                        max_pages_to_download)
        total_pages = max_pages_to_download
    else:
        print "Downloading All Pages"

    # Continue with remaining pages if first pass ok.
    if int(status) == 200 and total_pages > 1:
        for i in range(2, total_pages+1):
            soup, status = flickr_search_results_page(search_tag_term, i,
                                                      search_kwds)
            if int(status) != 200:
                print "Error on Page {}: Status Code {}".format(i, status)
                print "Print soup to determine problem."
                break
            picture_soup_data.extend(soup.findAll('photo'))
            if i % 1 == 0:
                sys.stdout.write("(----- {} Pages Downloaded -----)\r".format(i))
                sys.stdout.flush()
                # print ""
    print "Download COMPLETE                          "
    print ""
    return picture_soup_data


def flickr_search_results_page(search_tag_term, page_num, search_kwds):
    """Return a single API photo search results page."""
    search_url = 'https://api.flickr.com/services/rest/'
    search_kwds['page'] = page_num

    r = requests.get(search_url, params=search_kwds)
    soup = BeautifulSoup(r.text, 'lxml')

    return soup, r.status_code
