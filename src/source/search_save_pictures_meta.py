"""A Script to make a search request from Flickr API and save data to CSV."""
from flickr_api import get_flickr_keys, search_flicker
import sys
from save_data import create_dataframe_from_soup_objects, save_dataframe
from common.os_interaction import check_folder_exists


def get_keywords():
    """Produce default set of keywords for image search."""
    search_kwds = {'method': 'flickr.photos.search',
                   'api_key': flickr_keys['Key'],
                   'sort': 'relevance',
                   'content_type': '1',
                   'per_page': '500',
                   'license': '1, 2, 3, 4, 5, 6, 7',
                   'extras': 'license, owner_name, original_format, tags,\
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
    if len(sys.argv) == 2:
        print "\nWarning: [max_pages] Not Specified"
        print "--> Download Size May Be Large"
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
    # Check for and create if necessary the destination folder.
    check_folder_exists("data/tables/" + search_tag_term.upper())
    # Save all data to file.
    filename = 'data/tables/' + search_tag_term.upper()\
               + '/flickr_image_search_for_' \
               + search_tag_term.upper() + '_' + str(pages_searched)\
               + '.csv'
    save_dataframe(dataframe, filename)
