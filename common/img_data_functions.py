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


def get_rgb_counts(rgb_image_array, num_bins):
    """Ouput histographic arrays counting image RGB values."""
    red = rgb_image_array[:, :, 0].astype(int)
    green = rgb_image_array[:, :, 1].astype(int)
    blue = rgb_image_array[:, :, 2].astype(int)
    red_metrics = channel_metrics(red)
    green_metrics = channel_metrics(green)
    blue_metrics = channel_metrics(blue)
    red, red_centers = ski_exposure.histogram(red, nbins=num_bins)
    green, green_centers = ski_exposure.histogram(green, nbins=num_bins)
    blue, blue_centers = ski_exposure.histogram(blue, nbins=num_bins)
    return ((red, red_centers, red_metrics),
            (green, green_centers, green_metrics),
            (blue, blue_centers, blue_metrics))


def get_grey_counts(grey_image_array, num_bins):
    """Output histographic array counting image greyscale values."""
    grey = grey_image_array.astype(int)
    grey_metrics = channel_metrics(grey)
    grey, grey_centers = ski_exposure.histogram(grey, nbins=num_bins)
    return (grey, grey_centers, grey_metrics)


def get_luv_counts(luv_image_array, num_bins):
    """Ouput histographic arrays counting image RGB values."""
    l = luv_image_array[:, :, 0].astype(int)
    u = luv_image_array[:, :, 1].astype(int)
    v = luv_image_array[:, :, 2].astype(int)
    l_metrics = channel_metrics(l)
    u_metrics = channel_metrics(u)
    v_metrics = channel_metrics(v)
    l, l_centers = ski_exposure.histogram(l, nbins=num_bins)
    u, u_centers = ski_exposure.histogram(u, nbins=num_bins)
    v, v_centers = ski_exposure.histogram(v, nbins=num_bins)
    return ((l, l_centers, l_metrics),
            (u, u_centers, u_metrics),
            (v, v_centers, v_metrics))


def channel_metrics(array):
    """Produce common metrics for a color channel."""
    return array.max(), array.min(), np.mean(array), np.median(array)
