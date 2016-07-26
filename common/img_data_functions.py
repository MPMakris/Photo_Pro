"""A module with useful functions for manipulation of raw image data."""
from scipy import misc
from skimage import color as ski_color
import numpy as np


def read_image(filename):
    """Read an image from the disk and output data arrays."""
    image_array_rgb = misc.imread(filename, mode='RGB')
    image_array_grey = misc.imread(filename, flatten=True, mode='F')
    image_array_luv = ski_color.rgb2luv(image_array_rgb)
    return image_array_rgb, image_array_grey, image_array_luv


def get_channel_data(image_array, lower, upper, nbins):
    """
    Get channel feature data.

    INPUTS:
    image_array | 2D Numpy Array for a single channel.
    lower | Lowest allowable value in histogram results (integer).
    upper | Highest allowable value in histogram results (integer).
    nbins | Number of bins into which to split the data (integer).

    OUTPUTS:
    c_counts | A 1D Numpy Array of the counts of channel values in each bin.
    c_metrics | 1 1D Numpy Array of the metrics for the channel, in order:
                max, min, mean, median
    """
    c = image_array.astype(int)
    c_metrics = channel_metrics(c)
    c_counts = get_custom_hist(c, lower, upper, nbins)
    return c_counts, c_metrics


def get_custom_hist(array, lower, upper, nbins):
    """
    Get a histographic distribution of the array.

    INPUTS:
    array | 2D Numpy Array for a single channel.
    lower | Lowest allowable value in histogram results (integer).
    upper | Highest allowable value in histogram results (integer).
    nbins | Number of bins into which to split the data (integer).

    OUTPUT:
    counts | A 1D Numpy Array of the counts of channel values in each bin.
    """
    data = np.round(array.flatten(), decimals=0).astype(float)
    bin_width = ((upper+1) - lower)/float(nbins)
    steps = np.arange(lower, upper+1+bin_width, bin_width)
    counts = np.zeros((len(steps) - 1, ))
    for i, val in enumerate(steps[0:-1]):
        counts[i] = len(data[(data >= steps[i]) & (data < steps[i+1])])
    counts = counts[0:nbins+1].astype(int)
    return counts


def channel_metrics(array):
    """
    Produce common metrics for a color channel.

    INPUTS:
    array | 2D Numpy Array for a single channel.

    OUTPUT:
    metrics | A 1D Numpy Array of the metrics in order of:
              max, min, mean, median
    """
    return np.array([array.max(), array.min(), np.mean(array),
                     np.median(array)])
