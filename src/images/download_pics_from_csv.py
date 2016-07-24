"""A script for downloading images from Flickr."""
import sys
import pandas as pd
from common.os_interaction import get_file_name_from_path
from flickr_download import download_pics


def drop_duplicates(meta):
    """Drop any duplicates from the DataFrame and report number to download."""
    meta = meta[-meta.duplicated()].reset_index()
    print "\nUnique Photos to Download: {}".format(len(meta))
    return meta


if __name__ == '__main__':
    # Read User Imputs
    path = sys.argv[1]
    if len(sys.argv) > 2:
        size = sys.argv[2]
    else:
        size = 'h'
    if len(sys.argv) > 3:
        download_limit = int(sys.argv[3])
    else:
        download_limit = None
    # Determine Search_Term
    file_name = get_file_name_from_path(path)
    search_term = file_name[len('flickr_image_search_for_'):]
    search_term = search_term[:search_term.find('_')]
    # Read Meta Data
    df = pd.read_csv(path)
    df = drop_duplicates(df)
    # Download Pictures to Files
    download_pics(df, size, search_term, download_limit)
