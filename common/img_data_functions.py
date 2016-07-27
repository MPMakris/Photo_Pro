"""A module with useful functions for manipulation of raw image data."""
from scipy import misc
from skimage import color as ski_color
import numpy as np
from skimage import filters, feature
from sklearn.cluster import KMeans


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
    counts | A 1D Numpy Array of the density of channel values in each bin:
             (count/total_num)
    """
    data = np.round(array.flatten(), decimals=0).astype(float)
    bin_width = ((upper+1) - lower)/float(nbins)
    steps = np.arange(lower, upper+1+bin_width, bin_width)[0:nbins+1]
    counts = np.zeros((len(steps) - 1, ))
    for i, val in enumerate(steps[0:-1]):
        counts[i] = len(data[(data >= steps[i]) & (data < steps[i+1])])
    counts = counts[0:nbins+1]/len(data)
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


def calc_crispness(array):
    """
    Calculate the crispness of an image array.

    INPUTS:
    array | A 2D Numpy Array of the channel.

    OUTPUTS:
    crispness | A 1D Numpy Array of crispness measures in the channel of types:
                sobel, canny, laplace
    """
    array_scaled = array/255
    sobel_var = filters.sobel(array_scaled).var()
    canny_array = feature.canny(array_scaled, sigma=1).var()
    canny_ratio = np.sum(canny_array == True)/float(len(canny_array.flatten()))
    laplace_var = filters.laplace(array_scaled, ksize=3).var()
    return np.array([sobel_var, canny_ratio, laplace_var])


# def find_dominant_colors(color_array, num_colors):
#     """
#     Find the [num_colors] dominant colors in an RGB immage using KMeans cluter.
#
#     INPUTS:
#     color_array | A 3D Numpy Array of the RGB channels.
#     num_colors | Number of color centers to return.
#
#     OUTPUTS:
#     dom_colors | A 2D Numpy Array of the dominant RGB colors with shape:
#                  [num_colors, 3]
#     """
#     X = np.concatenate((color_array[:, :, 0].flatten().reshape((-1, 1)),
#                         color_array[:, :, 1].flatten().reshape((-1, 1)),
#                         color_array[:, :, 2].flatten().reshape((-1, 1))),
#                        axis=1)
#     model = KMeans(n_clusters=num_colors, n_jobs=1, n_init=4)
#     model.fit(X)
#     return model.cluster_centers_


def find_brightness_centers(grey_array, num_centers):
    """
    Find the [num_centers] brightness centers in an immage using KMeans cluter.

    INPUTS:
    grey_array | A 2D Numpy Array of the grey channel.
    num_centers | Number of brightness centers to return.

    OUTPUTS:
    centers | A 1D Numpy Array of the dominant brightness center values.
    """
    X = grey_array.flatten().reshape((-1, 1))
    model = KMeans(n_clusters=num_centers, n_jobs=1, n_init=4, random_state=42)
    model.fit(X)
    centers = model.cluster_centers_.reshape((-1, ))
    counts = get_custom_hist(model.labels_, 0, num_centers-1, num_centers)
    return centers[np.argsort(counts)[::-1]]


def find_aspect_ratio(array):
    """
    Find the aspect ratio of the image.

    INPUTS:
    array | A 2D Numpy Array of a channel.

    OUTPUTS:
    ratio | A float representing the aspect ratio of the image.
    """
    return array.shape[1]/float(array.shape[0])
