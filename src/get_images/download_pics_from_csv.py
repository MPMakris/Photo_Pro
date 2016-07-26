"""A script for downloading images from Flickr."""
import sys
import pandas as pd
from common.os_interaction import get_file_name_from_path
from flickr_download import download_pics


def drop_duplicates(meta):
    """Drop any duplicates from the DataFrame and report number to download."""
    meta = meta[-meta.duplicated()].reset_index(drop=True)
    print "\nUnique Photos to Download: {}".format(len(meta))
    return meta


def get_user_inputs(inputs):
    """Get user inputs from command line operation."""
    path = inputs[1]
    if len(inputs) > 2:
        size = inputs[2]
    else:
        size = 'h'
    if len(inputs) > 3:
        download_limit = int(inputs[3])
    else:
        download_limit = None
    return path, size, download_limit


def main(path, size, download_limit):
    """The main function for operating the script."""
    # Extract the Search Term
    file_name = get_file_name_from_path(path)
    search_term = file_name[len('flickr_image_search_for_'):]
    search_term = search_term[:search_term.find('_')]
    # Read Meta Data
    df = pd.read_csv(path, sep='|')
    df = drop_duplicates(df)
    # Download Pictures to Files
    download_pics(df, size, search_term, download_limit)

if __name__ == '__main__':
    # Read User Imputs:
    path, size, download_limit = get_user_inputs(sys.argv)
    # Run Script:
    main(path, size, download_limit)
