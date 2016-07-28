"""A module for storing common print functions for display on the cmd line."""
import sys


def print_download_page_status(page_count, status='200'):
    """
    Print an updating status message on the number of pages downloaded.

    INPUTS:
    page_count | Page number to print. (integer)
    status | A request object status code. (optional)

    OUTPUTS:
    None
    """
    if int(status) == 200:
        sys.stdout.write("(----- {} Pages Downloaded -----)\r".format(
                                                            page_count))
        sys.stdout.flush()
    else:
        sys.stdout.write("(----- {} Pages Downloaded -----)\n".format(
                                                            page_count - 1))
        sys.stdout.flush()
        print "Error on Page {:s}: Status Code {:s}".format(page_count, status)
        print "Print soup to determine problem."
