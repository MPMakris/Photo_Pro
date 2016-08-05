"""A module with useful functions for manipulation of raw image data."""
from scipy import misc
import numpy as np
from skimage import color


def read_image(filename):
    """Read an image from the disk and output data arrays."""
    image_array_rgb = misc.imread(filename, mode='RGB')
    #  image_array_grey = misc.imread(filename, flatten=True, mode='F')
    image_array_grey = color.rgb2grey(image_array_rgb)*255
    image_array_luv = color.rgb2luv(image_array_rgb)
    return image_array_rgb, image_array_grey, image_array_luv


def custom_hist(array, lower, upper, nbins, density=True):
    """Get histogram of values.

    PARAMETERS
    ----------
    channel_array : 1D or 2D numpy array
        Raw data values.

    lower : int
        Lower limit of data values allowed.

    upper : int
        Upper limit of data values allowed.

    nbins : int
        Number of bins to put data into.

    RETURNS
    -------
    counts : list
        A list of the counts of values in each bin.
    """
    values = array.astype(int).flatten()
    data = np.round(values, decimals=0).astype(float)
    bin_width = ((upper+1) - lower)/float(nbins)
    steps = np.arange(lower, upper+1+bin_width, bin_width)[0:nbins+1]
    hist, edges = np.histogram(data, bins=steps, density=density)
    return list(hist)
