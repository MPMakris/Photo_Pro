"""Saved methods for Flickr API use."""
import requests
from bs4 import BeautifulSoup
import sys
import datetime


def get_flickr_url():
    """Return Flicker API url."""
    return 'https://api.flickr.com/services/rest/'


def get_flickr_keys(filename='flickr.keys'):
    """Get the Ficker user and app keys from the .keys file."""
    flickr_keys = {}
    with open(filename) as f_open:
        key_list = f_open.read().split('\n')[0:2]
    for key in key_list:
        pair = key.split(":")
        flickr_keys[pair[0]] = pair[1]
    return flickr_keys


def print_download_status(status, count):
    """Print an updating status message."""
    if int(status) == 200:
        sys.stdout.write("(----- {} Pages Downloaded -----)\r".format(count))
        sys.stdout.flush()
    else:
        sys.stdout.write("(----- {} Pages Downloaded -----)\n".format(count-1))
        sys.stdout.flush()
        print "Error on Page {}: Status Code {}".format(count, status)
        print "Print soup to determine problem."


def get_info_from_result(soup):
    """Determine quantity of pages in search result."""
    pages = int(soup.photos.get('pages'))
    results = int(soup.photos.get('total'))
    return pages, results


def flickr_search(keywords, page_num=1):
    """Make a search of the Flickr API for photos matching [keywords] dict."""
    keywords['page'] = page_num
    search_url = get_flickr_url()
    r = requests.get(search_url, params=keywords)
    return BeautifulSoup(r.text, 'lxml'), r.status_code


def flickr_search_recursive_time(picture_soup, keywords, time_start, time_end,
                                 max_page, page_count=0):
    """Return a subset of the API search based on date range."""
    # Set the Time Bounds
    keywords['min_upload_date'] = str(time_start)
    keywords['max_upload_date'] = str(time_end)
    num_results_per_page = int(keywords['per_page'])
    # print "Recursive Search Start"
    # print "Page Count: {}".format(page_count)
    # print "Time Range: {} to {}".format(time_start, time_end)
    soup, status = flickr_search(keywords, page_num=1)
    num_pages, num_results = get_info_from_result(soup)
    # print "Num Results: {}".format(num_results)
    if num_results <= 4000:
        # If Less than 4000 Results, Proceed With Download
        for page in range(1, num_results/num_results_per_page+1+1):
            page_count += 1
            soup, status = flickr_search(keywords, page)
            print_download_status(status, page_count)
            if int(status) == 200:
                picture_soup.extend(soup.findAll('photo'))
            else:
                continue
            if page_count >= max_page:
                break
    else:
        # If More than 4000 Results, Split the Time Period in Half and Search
        time_mid = (time_end + time_start)/2
        picture_soup, page_count = flickr_search_recursive_time(
                                            picture_soup, keywords, time_mid+1,
                                            time_end, max_page, page_count)
        if page_count >= max_page:
            return picture_soup, page_count
        picture_soup, page_count = flickr_search_recursive_time(
                                            picture_soup, keywords, time_start,
                                            time_mid, max_page, page_count)
    return picture_soup, page_count


def search_flicker_complete(search_term, search_kwds, max_pages=None):
    """Search Flicker API for photos including a tagged term."""
    # Add Search Term to Keywords
    search_kwds['tags'] = search_term
    search_kwds['text'] = search_term
    # Add Time Limits to Keywords
    time_range_start = int(datetime.datetime(1970, 1, 1, 0, 0).strftime('%s'))
    time_range_end = int(datetime.datetime(2016, 7, 1, 0, 0).strftime('%s'))
    # Empty Object to Store All Incoming Data:
    picture_soup_data = []
    # Run a first pass to test results:
    soup, status = flickr_search(search_kwds, 1)
    if int(status) == 200:
        total_pages, total_results = get_info_from_result(soup)
        print "Search Results:  {} Pages Found | {} Images Found".format(
                                                    total_pages, total_results)
    else:
        print "Error: \tStatus Code {}".format(status)
        return None
    # Display Information to User
    if max_pages is not None:
        if max_pages < total_pages:
            print "Downloading First {} Pages of Results...".format(max_pages)
            total_pages = max_pages
    else:
        print "Downloading All Pages..."

    sys.stdout.write("(-----   Pre-Processing   -----)\r")
    sys.stdout.flush()
    # Begin Recursive Search through Time Chunks to Get all Pages
    picture_soup_data, page_returned = flickr_search_recursive_time(
                                            picture_soup_data, search_kwds,
                                            time_range_start, time_range_end,
                                            total_pages)
    print "Download COMPLETE                          \n"
    return picture_soup_data, page_returned
