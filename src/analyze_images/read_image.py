"""A script for reading a single image and creating features."""
from common.img_data_functions import read_image, get_channel_data
import numpy as np


def extract_channel_features(image_array, controls, lower, upper, nbins):
    """
    Produce the feature bins for a channel.

    image_array | 2D Nupy Array
    controls | Dictionary of feature creation controls.
    lower | Lower bound for the channel values to consider (integer).
    upper | Upper bound for the channel values to consider (integer).
    nbins | Number of bins into which channel values are divided (integer).
    """
    print "EXTRACTING COLOR"
    ((c1_counts, c1_centers, c1_metrics),
     (c2_counts, c2_centers, c2_metrics),
     (c3_counts, c3_centers, c3_metrics)) = get_color_counts(
                                                image_array_color, num_bins)
    print c1_counts.shape
    print c2_counts.shape
    print c3_counts.shape
    print c1_metrics.shape
    print c2_metrics.shape
    print c3_metrics.shape
    channel_data = np.concatenate((c1_counts, c2_counts, c3_counts))
    if controls['create_max']:
        channel_data = np.concatenate((channel_data, np.array([c1_metrics[0],
                                       c2_metrics[0], c3_metrics[0]])))
    if controls['create_min']:
        channel_data = np.concatenate((channel_data, np.array([c1_metrics[1],
                                       c2_metrics[1], c3_metrics[1]])))
    if controls['create_mean']:
        channel_data = np.concatenate((channel_data, np.array([c1_metrics[2],
                                       c2_metrics[2], c3_metrics[2]])))
    if controls['create_median']:
        channel_data = np.concatenate((channel_data, np.array([c1_metrics[3],
                                       c2_metrics[3], c3_metrics[3]])))
    print "Channel_Data Shape: {}".format(channel_data.shape)
    return channel_data, np.concatenate((c1_centers, c2_centers, c3_centers))


def extract_grey_channel_features(image_array_grey, controls, num_bins):
    """Produce Numpy.Array of grety channel feature data."""
    (grey_counts, grey_centers, grey_metrics) = get_grey_counts(
                                                image_array_grey, num_bins)
    print "EXTRACTING GREYSCALE"
    print grey_counts.shape
    print grey_metrics.shape
    channel_data = grey_counts
    if controls['create_max']:
        channel_data = np.append(channel_data, grey_metrics[0])
    if controls['create_min']:
        channel_data = np.append(channel_data, grey_metrics[1])
    if controls['create_mean']:
        channel_data = np.append(channel_data, grey_metrics[2])
    if controls['create_median']:
        channel_data = np.append(channel_data, grey_metrics[3])
    print "Channel_Data Shape: {}".format(channel_data.shape)
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
        print "AFTER RGB: {}".format(image_data.shape)
    if controls['enable_grey']:
        channel_data, center_data = extract_grey_channel_features(
                                        image_array_grey, controls, num_bins)
        image_data = np.append(image_data, channel_data)
        image_center_data = np.append(image_center_data, center_data)
        print "AFTER GREY: {}".format(image_data.shape)
    if controls['enable_luv']:
        channel_data, center_data = extract_color_channels_features(
                                        image_array_luv, controls, num_bins)
        image_data = np.append(image_data, channel_data)
        image_center_data = np.append(image_center_data, center_data)
        print "AFTER LUV: {}".format(image_data.shape)
    print "TOTAL AFTER BIN SIZE RUN: {}".format(image_data.shape)
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
    print "Image Data New Part: {}".format(image_data_bin.shape)
    image_data = np.append(image_data, image_data_bin)
    print "Image Data Whole: {}".format(image_data.shape)
    image_bin_centers = np.append(image_bin_centers, image_center_data_bin)
    # Medium-Size Bins:
    num_bins = controls['medium_bins']
    image_data_bin, image_center_data_bin = extract_for_bin_size(
        image_array_rgb, image_array_grey, image_array_luv, num_bins, controls)
    print "Image Data New Part: {}".format(image_data_bin.shape)
    image_data = np.append(image_data, image_data_bin)
    print "Image Data Whole: {}".format(image_data.shape)
    image_bin_centers = np.append(image_bin_centers, image_center_data_bin)
    # Large-Size Bins:
    num_bins = controls['large_bins']
    image_data_bin, image_center_data_bin = extract_for_bin_size(
        image_array_rgb, image_array_grey, image_array_luv, num_bins, controls)
    print "Image Data New Part: {}".format(image_data_bin.shape)
    image_data = np.append(image_data, image_data_bin)
    print "Image Data Whole: {}".format(image_data.shape)
    image_bin_centers = np.append(image_bin_centers, image_center_data_bin)
    return image_data, image_bin_centers
