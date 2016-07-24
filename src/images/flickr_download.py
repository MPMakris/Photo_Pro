"""Functions for downloading images from Flickr."""
from common.os_interaction import check_folder_exists
import requests
import shutil


def check_image_returned_ok(r):
    """Check to see if the returned image is a real photo or unavailable."""
    return not r.url.find('photo_unavailable') > 0


def assemble_info(df, i, size):
    """Create the request url and filename from meta data."""
    url = "https://farm{}.staticflickr.com/{}/{}_{}_{}.{}".format(
                                                df.loc[i, :]['farm'],
                                                df.loc[i, :]['server'],
                                                df.loc[i, :]['id'],
                                                df.loc[i, :]['secret'],
                                                size,
                                                df.loc[i, :]['originalformat'])
    file_name = '{}_{}.jpg'.format(df.loc[i, :]['owner'], df.loc[i, :]['id'])
    return url, file_name


def download_pic(df, i, size, destination):
    """Download a picture based on the meta data in the Dataframe [df]."""
    url, file_name = assemble_info(df, i, size)
    dest_folder = 'data/images/{}/'.format(destination)
    path_name = dest_folder + file_name
    # Perform the request.
    r = requests.get(url, stream=True)
    # Check if the image returned is Flickr's standard unavailable image.
    if not check_image_returned_ok(r):
        print "Image [{}] Not Downloaded, Photo Unavailable".format(file_name)
        return 1  # Indicates picture did not download.
    check_folder_exists(dest_folder)
    # Write the raw image data to the file.
    with open(path_name, 'wb') as out_file:
        shutil.copyfileobj(r.raw, out_file)
    del r
    return 0  # Indicates that picture successfully downloaded.


def download_pics(df, size, search_term, download_limit):
    """Download all pictures in the DataFrame."""
    print "Downloading Images..."
    total = len(df)
    total_failed = 0
    total_downloaded = 0
    if download_limit is not None:
        limit = download_limit
    else:
        limit = total
    for i in xrange(limit):
        result = download_pic(df, i, size, search_term)
        print result
        total_failed += result
        total_downloaded += [1 if res == 0 else 0 for res in [result]][0]
        print "--> {} Percent Complete".format(int(i/total*100))
    destination = 'data/images/{}/'.format(search_term)
    print "{} Images Successfully Downlaoded to {}".format(total_downloaded,
                                                           destination)
    print "{} Images Did Not Download".format(total_failed)
