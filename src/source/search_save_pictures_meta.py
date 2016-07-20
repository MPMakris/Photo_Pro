"""A Script to make a search request from Flickr API and save data to CSV."""
from flickr_api import get_flickr_keys, search_flicker
import sys
from save_data import create_dataframe_from_soup_objects, save_dataframe


def get_keywords():
    """Produce default set of keywords for image search."""
    search_kwds = {'method': 'flickr.photos.search',
                   'api_key': flickr_keys['Key'],
                   'sort': 'relevance',
                   'content_type': '1',
                   'per_page': '500',
                   'extras': 'license, owner_name, original_format, geo, tags,\
                              o_dims, views, url_o, date_upload, date_taken'
                   }
    return search_kwds

if __name__ == '__main__':
    """
    Argv0: This File
    Argv1: Search Word
    Argv2: Max Number of Pages to Download (Optional)
    """
    search_tag_term = 'Search Tag is entered incorrectly.'
    max_pages_to_download = None
    # Get user inputs:
    search_tag_term = sys.argv[1]
    if len(sys.argv) >= 3:
        max_pages_to_download = int(sys.argv[2])
    # Get api_keys and keywords to search:
    flickr_keys = get_flickr_keys('flickr.keys')
    search_kwds = get_keywords()
    # Search for and save picture metadata:
    print "\nBegin Flickr Image Search For {}:".format(search_tag_term.upper())
    picture_soup_data, pages_searched = search_flicker(search_tag_term,
                                                       search_kwds,
                                                       max_pages_to_download)
    print "Creating DataFrame:"
    dataframe = create_dataframe_from_soup_objects(picture_soup_data)
    filename = 'data/tables/flickr_image_search_for_' \
               + search_tag_term.upper() + '_' + str(pages_searched) + '.csv'
    save_dataframe(dataframe, filename)
