"""A script for reading a single image and creating features."""
from common.img_data_functions import read_image, get_channel_data
from common.os_interaction import get_file_name_from_path
from common.img_meta_functions import split_img_name
import numpy as np


def filter_metrics(metrics, controls):
    """
    Return only the metrics requested in the control dictionary.

    INPUTS:
    metrics | A 1D Numpy Array with all metric information.
    controls | A Dictionary containing feature control information.

    OUTPUTS:
    metrics | A 1D Numpy Array with only the requested metrics included.
    """
    return (metrics[np.array([controls['create_max'], controls['create_min'],
            controls['create_mean'], controls['create_median']])])


def extract_for_bin_size(image_array_rgb, image_array_grey, image_array_luv,
                         nbins, controls):
    """
    Extract image channel features given a variable bin (DICT) quantity.

    INPUTS:
    image_array_rgb | A 3D Numpy array of of the RGB image data.
    image_array_grey | A 2D Numpy array of of the Greyscale image data.
    image_array_luv | A 3D Numpy array of of the LUV image data.
    nbins | A Dictionary of nbin values, with the channel type as the key.
            Example: nbins = {'rgb': 255, 'grey': 255, 'l': 100, 'uv': 200}
    controls | A Dictionary containing feature control information.

    OUTPUTS:
    image_feature_data | A 1D Numpy Array of all the concatenated feature data.
    """
    # Set Up Empty Array for Incoming Feature Data:
    image_feature_data = np.empty((1, 0))
    # Extract Image Feature Data
    if controls['enable_rgb']:
        num_bins = nbins['rgb']
        red_counts, red_metrics = get_channel_data(image_array_rgb[:, :, 0],
                                                   0, 255, num_bins)
        green_counts, green_metrics = get_channel_data(image_array_rgb[:, :, 1],
                                                       0, 255, num_bins)
        blue_counts, blue_metrics = get_channel_data(image_array_rgb[:, :, 2],
                                                     0, 255, num_bins)
        rgb_features = np.concatenate((red_counts,
                                      filter_metrics(red_metrics, controls),
                                      green_counts,
                                      filter_metrics(green_metrics, controls),
                                      blue_counts,
                                      filter_metrics(blue_metrics, controls)))
        image_feature_data = np.append(image_feature_data, rgb_features)
        # print "AFTER RGB: {}".format(image_feature_data.shape)
    if controls['enable_grey']:
        num_bins = nbins['grey']
        grey_counts, grey_metrics = get_channel_data(image_array_grey, 0, 255,
                                                     num_bins)
        grey_features = np.concatenate((grey_counts,
                                       filter_metrics(grey_metrics, controls)))
        image_feature_data = np.append(image_feature_data, grey_features)
        # print "AFTER GREY: {}".format(image_feature_data.shape)
    if controls['enable_luv']:
        num_bins_l = nbins['l']
        num_bins = nbins['uv']
        l_counts, l_metrics = get_channel_data(image_array_luv[:, :, 0],
                                               0, 100, num_bins_l)
        # print "L features: {} {}".format(l_counts.shape, l_metrics.shape)
        u_counts, u_metrics = get_channel_data(image_array_luv[:, :, 1],
                                               -100, 100, num_bins)
        # print "U features: {} {}".format(u_counts.shape, u_metrics.shape)
        v_counts, v_metrics = get_channel_data(image_array_luv[:, :, 2],
                                               -100, 100, num_bins)
        # print "V features: {} {}".format(v_counts.shape, v_metrics.shape)
        luv_features = np.concatenate((l_counts,
                                      filter_metrics(l_metrics, controls),
                                      u_counts,
                                      filter_metrics(u_metrics, controls),
                                      v_counts,
                                      filter_metrics(v_metrics, controls)))
        image_feature_data = np.append(image_feature_data, luv_features)
    #     print "AFTER LUV: {}".format(image_feature_data.shape)
    # print "TOTAL AFTER BIN SIZE RUN: {}".format(image_feature_data.shape)
    return image_feature_data


def analyze_image(image_path, controls):
    """
    Produce the total feature row data for a single image.

    INPUTS:
    image_path | String representation of image location on disk.
    controls | A Dictionary containing feature control information.

    OUTPUT:
    image_data | A 1D Numpy Array of all the concatenated feature data.
    """
    # Get File Owner and ID Fields:
    image_name = get_file_name_from_path(image_path)
    owner, ID = split_img_name(image_name)
    # Prep Array to Hold data
    image_data = np.array([owner, ID])
    # Read in Raw Image Channel Arrays
    image_array_rgb, image_array_grey, image_array_luv = read_image(image_path)
    # Get Featurized Data from Raw Image Channel Arrays
    if controls['discreet_bins']:
        nbins = controls['discreet_nbins']
        image_data = np.append(image_data, extract_for_bin_size(
                                            image_array_rgb, image_array_grey,
                                            image_array_luv, nbins, controls))
    if controls['medium_bins']:
        nbins = controls['medium_nbins']
        image_data = np.append(image_data, extract_for_bin_size(
                                            image_array_rgb, image_array_grey,
                                            image_array_luv, nbins, controls))
    if controls['large_bins']:
        nbins = controls['large_nbins']
        image_data = np.append(image_data, extract_for_bin_size(
                                            image_array_rgb, image_array_grey,
                                            image_array_luv, nbins, controls))
    return image_data
