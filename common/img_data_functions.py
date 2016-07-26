"""A module with useful functions for manipulation of raw image data."""
from scipy import misc
from skimage import exposure as ski_exposure, color as ski_color
import numpy as np


def read_image(filename):
    """Read an image from the disk and output data arrays."""
    image_array_rgb = misc.imread(filename, mode='RGB')
    image_array_grey = misc.imread(filename, flatten=True, mode='F')
    image_array_luv = ski_color.rgb2luv()
    return image_array_rgb, image_array_grey, image_array_luv


def get_color_counts(color_image_array, num_bins):
    """Ouput histographic arrays counting image RGB values."""
    c1 = color_image_array[:, :, 0].astype(int)
    c2 = color_image_array[:, :, 1].astype(int)
    c3 = color_image_array[:, :, 2].astype(int)
    c1_metrics = channel_metrics(c1)
    c2_metrics = channel_metrics(c2)
    c3_metrics = channel_metrics(c3)
    c1, c1_centers = ski_exposure.histogram(c1, nbins=num_bins)
    c2, c2_centers = ski_exposure.histogram(c2, nbins=num_bins)
    c3, c3_centers = ski_exposure.histogram(c3, nbins=num_bins)
    return ((c1, c1_centers, c1_metrics),
            (c2, c2_centers, c2_metrics),
            (c3, c3_centers, c3_metrics))


def get_grey_counts(grey_image_array, num_bins):
    """Output histographic array counting image greyscale values."""
    grey = grey_image_array.astype(int)
    grey_metrics = channel_metrics(grey)
    grey, grey_centers = ski_exposure.histogram(grey, nbins=num_bins)
    return (grey, grey_centers, grey_metrics)


# def get_luv_counts(luv_image_array, num_bins):
#     """Ouput histographic arrays counting image RGB values."""
#     l = luv_image_array[:, :, 0].astype(int)
#     u = luv_image_array[:, :, 1].astype(int)
#     v = luv_image_array[:, :, 2].astype(int)
#     l_metrics = channel_metrics(l)
#     u_metrics = channel_metrics(u)
#     v_metrics = channel_metrics(v)
#     l, l_centers = ski_exposure.histogram(l, nbins=num_bins)
#     u, u_centers = ski_exposure.histogram(u, nbins=num_bins)
#     v, v_centers = ski_exposure.histogram(v, nbins=num_bins)
#     return ((l, l_centers, l_metrics),
#             (u, u_centers, u_metrics),
#             (v, v_centers, v_metrics))


def channel_metrics(array):
    """Produce common metrics for a color channel."""
    return np.array([array.max(), array.min(), np.mean(array),
                     np.median(array)])
