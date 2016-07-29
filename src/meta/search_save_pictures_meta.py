"""A Script to make a search request from Flickr API and save data to CSV."""
from flickr_api import search_flicker_complete
import sys
from save_data import create_dataframe_from_soup_objects, save_dataframe
from common.os_interaction import check_folder_exists
from common.flickr_api_functions import get_flickr_keys


def get_keywords(api_keys):
    """Produce default set of keywords for image search."""
    search_kwds = {'method': 'flickr.photos.search',
                   'api_key': api_keys['Key'],
                   'sort': 'relevance',
                   'content_type': '1',
                   'per_page': '500',
                   'license': '1, 2, 3, 4, 5, 6, 7',
                   'extras': 'license, owner_name, original_format, tags,\
                              o_dims, views, url_o, date_upload, date_taken'
                   }
    return search_kwds


def main(search_term, max_pages):
    """Main function called during script."""
    # Get api_keys and keywords to search:
    flickr_keys = get_flickr_keys('flickr.keys')
    search_kwds = get_keywords(flickr_keys)
    # Search for and save picture metadata:
    print "\nBegin Flickr Image Search For {}:".format(search_term.upper())
    picture_soup, pages_searched = search_flicker_complete(search_term,
                                                           search_kwds,
                                                           max_pages)
    print "Creating DataFrame:"
    dataframe = create_dataframe_from_soup_objects(picture_soup)
    # Check for and create if necessary the destination folder.
    directory = "data/meta/"
    check_folder_exists(directory + search_term.upper())
    # Save all data to file.
    filename = (directory + search_term.upper() +
                '/flickr_image_search_for_' +
                search_term.upper() + '_' + str(pages_searched) +
                '.csv')
    save_dataframe(dataframe, filename)

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
    main(search_tag_term, max_pages_to_download)
