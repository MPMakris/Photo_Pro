"""A module for storing common Flickr API functions."""
import requests
from bs4 import BeautifulSoup
import pandas as pd


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


def get_user_data(user_id):
    """
    Get data from Flickr API about the user.

    INPUTS:
    user_id | A user NSID number. (string)

    OUTPUTS:
    user_stats | A Pandas Series of the following user statistics:
                 is_pro (int bool)
                 can_buy_pro (int bool)
                 gender (string)
                 total_views (int)
    """
    url = get_flickr_url()
    api_keys = get_flickr_keys()
    # Method: flickr.people.getInfo
    params = {'method': 'flickr.people.getInfo',
              'api_key': api_keys['Key'],
              'user_id': user_id
              }
    soup = BeautifulSoup(requests.get(url, params=params).content, 'lxml')
    is_pro = int(soup.person.get('ispro'))
    can_buy_pro = int(soup.person.get('can_buy_pro'))
    total_views = int(soup.count.contents[0])
    return pd.Series(data=[is_pro, can_buy_pro, total_views])


def get_image_data(image_id):
    """
    Get data from Flickr API about the image.

    INPUTS:
    image_id | An image ID number. (string)

    OUTPUTS:
    image_stats | A 1D Numpy Array of the following user statistics:
                 is_pro (int bool)
                 can_buy_pro (int bool)
                 gender (string)
                 total_views (int)
    """
    url = get_flickr_url()
    api_keys = get_flickr_keys()
    params = {'method': None,
              'api_key': api_keys['Key'],
              'photo_id': image_id
              }
    print "test"
    #  Method: flickr.photos.comments.getList
    params['method'] = 'flickr.photos.comments.getList'
    soup = BeautifulSoup(requests.get(url, params=params).content, 'lxml')
    image_ncomments = len(soup.findAll('comment'))
    #  Method: flickr.photos.getFavorites
    params['method'] = 'flickr.photos.getFavorites'
    soup = BeautifulSoup(requests.get(url, params=params).content, 'lxml')
    image_nfavs = soup.photo.get('total')
    #  Method: flickr.photos.getAllContexts
    params['method'] = 'flickr.photos.getAllContexts'
    soup = BeautifulSoup(requests.get(url, params=params).content, 'lxml')
    image_nsets = len(soup.findAll('set'))
    image_npools = len(soup.findAll('pool'))
    return pd.Series(data=[image_ncomments, image_nfavs, image_nsets,
                           image_npools])
