"""A script for reading a single image and creating features."""
from common.img_data_functions import (read_image, get_color_counts,
                                       get_grey_counts)
import numpy as np


def extract_color_channels_features(image_array_color, controls, num_bins):
    """Produce Numpy.Array of color (RGB or LUV) channels feature data."""
    ((c1_counts, c1_centers, c1_metrics),
     (c2_counts, c2_centers, c2_metrics),
     (c3_counts, c3_centers, c3_metrics)) = get_color_counts(
                                                image_array_color, num_bins)
    channel_data = np.concatenate((c1_counts, c2_counts, c3_counts))
    if controls['create_max']:
        channel_data = np.concatenate((channel_data, c1_metrics[0],
                                       c2_metrics[0], c3_metrics[0]))
    if controls['create_min']:
        channel_data = np.concatenate((channel_data, c1_metrics[1],
                                       c2_metrics[1], c3_metrics[1]))
    if controls['create_mean']:
        channel_data = np.concatenate((channel_data, c1_metrics[2],
                                       c2_metrics[2], c3_metrics[2]))
    if controls['create_median']:
        channel_data = np.concatenate((channel_data, c1_metrics[3],
                                       c2_metrics[3], c3_metrics[3]))
    return channel_data, np.concatenate((c1_centers, c2_centers, c3_centers))


def extract_grey_channel_features(image_array_grey, controls, num_bins):
    """Produce Numpy.Array of grety channel feature data."""
    channel_data = np.empty((1, 0))
    (grey_counts, grey_centers, grey_metrics) = get_grey_counts(
                                                image_array_grey, num_bins)
    channel_data = np.append(channel_data, grey_counts)
    if controls['create_max']:
        channel_data = np.append(channel_data, grey_metrics[0])
    if controls['create_min']:
        channel_data = np.append(channel_data, grey_metrics[1])
    if controls['create_mean']:
        channel_data = np.append(channel_data, grey_metrics[2])
    if controls['create_median']:
        channel_data = np.append(channel_data, grey_metrics[3])
    return channel_data, grey_centers


def extract_for_bin_size(image_array_rgb, image_array_grey, image_array_luv,
                         num_bins, controls):
    """Extract information given a variable bin quantity."""
    image_data = np.empty((1, 0))
    image_center_data = np.empty((1, 0))
    if controls['enable_rgb']:
        channel_data, center_data = extract_color_channels_features(
                                        image_array_rgb, controls, num_bins)
        image_data = np.append(image_data, channel_data)
        image_center_data = np.append(image_center_data, center_data)
    if controls['enable_grey']:
        channel_data, center_data = extract_grey_channel_features(
                                        image_array_grey, controls, num_bins)
        image_data = np.append(image_data, channel_data)
        image_center_data = np.append(image_center_data, center_data)
    if controls['enable_luv']:
        channel_data, center_data = extract_color_channels_features(
                                        image_array_luv, controls, num_bins)
        image_data = np.append(image_data, channel_data)
        image_center_data = np.append(image_center_data, center_data)
    return image_data, image_center_data


def analyze_image(image_path, controls):
    """Produce the total feature row data for a single image."""
    # Prep Array to Hold data
    image_data = np.empty((1, 0))
    image_bin_centers = np.empty((1, 0))
    # Read in Raw Image Channel Arrays
    image_array_rgb, image_array_grey, image_array_luv = read_image(image_path)
    # Get Featurized Data from Raw Image Channel Arrays
    # Discreet-Size Bins:
    num_bins = controls['discreet_bins']
    image_data_bin, image_center_data_bin = extract_for_bin_size(
        image_array_rgb, image_array_grey, image_array_luv, num_bins, controls)
    image_data = np.append(image_data, image_data_bin)
    image_bin_centers = np.append(image_bin_centers, image_center_data_bin)
    # Medium-Size Bins:
    num_bins = controls['medium_bins']
    image_data_bin, image_center_data_bin = extract_for_bin_size(
        image_array_rgb, image_array_grey, image_array_luv, num_bins, controls)
    image_data = np.append(image_data, image_data_bin)
    image_bin_centers = np.append(image_bin_centers, image_center_data_bin)
    # Large-Size Bins:
    num_bins = controls['large_bins']
    image_data_bin, image_center_data_bin = extract_for_bin_size(
        image_array_rgb, image_array_grey, image_array_luv, num_bins, controls)
    image_data = np.append(image_data, image_data_bin)
    image_bin_centers = np.append(image_bin_centers, image_center_data_bin)
    return image_data, image_bin_centers
