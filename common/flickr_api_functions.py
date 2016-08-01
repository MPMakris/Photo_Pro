"""A module for storing common Flickr API functions."""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
from time import sleep


def get_flickr_url():
    """Return Flicker API url as a string."""
    return 'https://api.flickr.com/services/rest/'


def get_flickr_keys(filename='flickr.keys'):
    """Get the Ficker user and app keys from the private .keys file."""
    flickr_keys = {}
    with open(filename) as f_open:
        key_list = f_open.read().split('\n')[0:2]
    for key in key_list:
        pair = key.split(":")
        flickr_keys[pair[0]] = pair[1]
    return flickr_keys


def get_user_data(user_info):
    """
    Get data from Flickr API about the user.

    INPUTS:
    user_info | A Pandas Series containing an index and a user NSID number:
                (int, string)

    OUTPUTS:
    user_stats | A Pandas Series of the following user statistics:
                 is_pro (int bool)
                 can_buy_pro (int bool)
                 gender (string)
                 total_views (int)
    """
    image_idx = int(user_info[0]) + 1
    user_id = user_info[1]
    url = get_flickr_url()
    api_keys = get_flickr_keys()
    # Method: flickr.people.getInfo
    params = {'method': 'flickr.people.getInfo',
              'api_key': api_keys['Key'],
              'user_id': user_id
              }
    try:
        soup = BeautifulSoup(requests.get(url, params=params).content, 'lxml')
        is_pro = int(soup.person.get('ispro'))
        can_buy_pro = int(soup.person.get('can_buy_pro'))
        total_views = int(soup.count.contents[0])
    except (AttributeError, requests.ConnectionError):
        sleep(2)
        try:
            soup = BeautifulSoup(requests.get(url, params=params).content,
                                 'lxml')
            is_pro = int(soup.person.get('ispro'))
            can_buy_pro = int(soup.person.get('can_buy_pro'))
            total_views = int(soup.count.contents[0])
        except (AttributeError, requests.ConnectionError):
            is_pro = "NaN"
            can_buy_pro = "NaN"
            total_views = "NaN"
    sys.stdout.write(
        "\rRun: \033[1;35m{}\033[0m for User: \033[1;35m{}\033[0m".format(
                                                          image_idx, user_id))
    sys.stdout.flush()
    return pd.Series(data=[is_pro, can_buy_pro, total_views])


def get_image_data(image_info):
    """
    Get data from Flickr API about the image.

    INPUTS:
    image_info | A Pandas Series containing an index and an image ID number:
                 (int, string)

    OUTPUTS:
    image_stats | A 1D Numpy Array of the following user statistics:
                 is_pro (int bool)
                 can_buy_pro (int bool)
                 gender (string)
                 total_views (int)
    """
    image_idx = int(image_info[0]) + 1
    image_id = image_info[1]
    url = get_flickr_url()
    api_keys = get_flickr_keys()
    params = {'method': None,
              'api_key': api_keys['Key'],
              'photo_id': int(str(image_id).strip(" "))
              }
    #  Method: flickr.photos.comments.getList
    params['method'] = 'flickr.photos.comments.getList'
    try:
        soup = BeautifulSoup(requests.get(url, params=params).content, 'lxml')
        image_ncomments = len(soup.findAll('comment'))
    except (AttributeError, requests.ConnectionError):
        sleep(2)
        try:
            soup = BeautifulSoup(requests.get(url, params=params).content,
                                 'lxml')
            image_ncomments = len(soup.findAll('comment'))
        except (AttributeError, requests.ConnectionError):
            image_ncomments = "NaN"
    #  Method: flickr.photos.getFavorites
    params['method'] = 'flickr.photos.getFavorites'
    try:
        soup = BeautifulSoup(requests.get(url, params=params).content, 'lxml')
        image_nfavs = soup.photo.get('total')
    except (AttributeError, requests.ConnectionError):
        sleep(2)
        try:
            soup = BeautifulSoup(requests.get(url, params=params).content,
                                 'lxml')
            image_nfavs = soup.photo.get('total')
        except (AttributeError, requests.ConnectionError):
            image_nfavs = "NaN"
    #  Method: flickr.photos.getAllContexts
    params['method'] = 'flickr.photos.getAllContexts'
    try:
        soup = BeautifulSoup(requests.get(url, params=params).content, 'lxml')
        image_nsets = len(soup.findAll('set'))
        image_npools = len(soup.findAll('pool'))
    except (AttributeError, requests.ConnectionError):
        sleep(2)
        try:
            soup = BeautifulSoup(requests.get(url, params=params).content,
                                 'lxml')
            image_nsets = len(soup.findAll('set'))
            image_npools = len(soup.findAll('pool'))
        except (AttributeError, requests.ConnectionError):
            image_nsets = "NaN"
            image_npools = "NaN"
    #  Method: flickr.photos.getInfo
    params['method'] = 'flickr.photos.getInfo'
    try:
        soup = BeautifulSoup(requests.get(url, params=params).content, 'lxml')
        image_views = soup.photo.get('views')
        image_tags = [tag.get('raw') for tag in soup.findAll('tag')]
        image_ntags = len(image_tags)
    except (AttributeError, requests.ConnectionError):
        sleep(2)
        try:
            soup = BeautifulSoup(requests.get(url, params=params).content,
                                 'lxml')
            image_views = soup.photo.get('views')
            image_tags = [tag.get('raw') for tag in soup.findAll('tag')]
            image_ntags = len(image_tags)
        except (AttributeError, requests.ConnectionError):
            image_views = "NaN"
            image_tags = "NaN"
            image_ntags = "NaN"
    #  Print Status Message
    sys.stdout.write(
        "\rRun: \033[1;35m{}\033[0m for Image: \033[1;35m{}\033[0m".format(
                                                         image_idx, image_id))
    sys.stdout.flush()
    return pd.Series(data=[image_ncomments, image_nfavs, image_nsets,
                           image_npools, image_views, image_ntags, image_tags])
