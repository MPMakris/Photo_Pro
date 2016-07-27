"""A script for reading a single image and creating features."""
from common.img_data_functions import (read_image, get_channel_data,
                                       find_aspect_ratio, calc_crispness,
                                       find_brightness_centers)
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


def get_column_bin_names(controls, color, nbins):
    """
    Return the metric names to be included in the feature matrix.

    INPUTS:
    controls | The feature control dictionary.
    color | Name of the color the metric applies to (string).
    nbins | Number of bins for which the metric was calculated (int).

    OUPUTS:
    metric_names | A 1D Numpy Array of the metric names as strings.
    """
    column_bin_names = np.empty((1, 0))
    for i in range(1, nbins+1):
        column_bin_names = np.append(column_bin_names,
                                     "{}_bin{}_nbins{}".format(color, i,
                                                               str(nbins)))
    if controls['create_max']:
        column_bin_names = np.append(column_bin_names,
                                     "{}_max_nbins{}".format(color,
                                                             str(nbins)))
    if controls['create_min']:
        column_bin_names = np.append(column_bin_names,
                                     "{}_min_nbins{}".format(color,
                                                             str(nbins)))
    if controls['create_mean']:
        column_bin_names = np.append(column_bin_names,
                                     "{}_mean_nbins{}".format(color,
                                                              str(nbins)))
    if controls['create_median']:
        column_bin_names = np.append(column_bin_names,
                                     "{}_median_nbins{}".format(color,
                                                                str(nbins)))
    return column_bin_names


def get_columns_for_bin_class(controls, bin_class):
    """
    Get column names for a class of bin size.

    INPUTS:
    controls | The feature control dictionary.
    bin_class | A string pointing to a bin class.

    OUTPUTS:
    bin_class_column_names | Column names for the channels called in the class.
    """
    bin_class_column_names = np.empty((1, 0))
    if controls['enable_rgb']:
        for color in ['red', 'green', 'blue']:
            num_bins = controls[bin_class]['rgb']
            bin_class_column_names = np.append(bin_class_column_names,
                                               get_column_bin_names(controls,
                                                                    color,
                                                                    num_bins))
    if controls['enable_grey']:
        for color in ['grey']:
            num_bins = controls[bin_class]['grey']
            bin_class_column_names = np.append(bin_class_column_names,
                                               get_column_bin_names(controls,
                                                                    color,
                                                                    num_bins))
    if controls['enable_luv']:
        for color in ['l']:
            num_bins = controls[bin_class]['l']
            bin_class_column_names = np.append(bin_class_column_names,
                                               get_column_bin_names(controls,
                                                                    color,
                                                                    num_bins))
    if controls['enable_luv']:
        for color in ['u', 'v']:
            num_bins = controls[bin_class]['uv']
            bin_class_column_names = np.append(bin_class_column_names,
                                               get_column_bin_names(controls,
                                                                    color,
                                                                    num_bins))
    return bin_class_column_names


def get_brightness_columns(num_centers):
    """
    Get the list of column names for a given [num_centers].

    INPUTS:
    num_centers | The number of brightness centers determined (int).

    OUPUTS:
    center_column_names | A 1D Numpy Array of column names.
    """
    center_column_names = np.empty((1, 0))
    for i in range(1, num_centers+1):
        center_column_names = np.append(center_column_names,
                                        "bright_ctr{}_numctrs{}".format(
                                                            i, num_centers))
    return center_column_names

def extract_for_bin_size(image_array_rgb, image_array_grey, image_array_luv,
                         bin_class, controls):
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
    nbins = controls[bin_class]
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


def analyze_image(image_path, controls, return_col_names):
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
    column_names = np.array(['owner', 'id'])
    # Read in Raw Image Channel Arrays
    image_array_rgb, image_array_grey, image_array_luv = read_image(image_path)
    # Get Featurized Data from Raw Image Channel Arrays
    for bin_class in ['discreet_bins', 'medium_bins', 'large_bins']:
        if controls[bin_class]:
            image_data = np.append(image_data,
                                   extract_for_bin_size(image_array_rgb,
                                                        image_array_grey,
                                                        image_array_luv,
                                                        bin_class,
                                                        controls))
            if return_col_names:
                column_names = np.append(column_names,
                                         get_columns_for_bin_class(controls,
                                                                   bin_class))
    if controls['find_crispnesses']:
        image_data = np.append(image_data, calc_crispness(image_array_grey))
        if return_col_names:
            column_names = np.append(column_names,
                                     np.array(['crisp_sobel', 'crisp_canny',
                                               'script']))
    if controls['find_aspect_ratio']:
        image_data = np.append(image_data, find_aspect_ratio(image_array_grey))
        if return_col_names:
            column_names = np.append(column_names, 'aspect_ratio')
    if controls['find_dominant_colors']:
        for num_colors in controls['dom_colors_try']:
            # Replaced by Find Brightness Centers
            pass
    if controls['find_brightness_centers']:
        for num_centers in controls['bright_centers_try']:
            image_data = np.append(image_data,
                                   find_brightness_centers(image_array_grey,
                                                           num_centers))
            if return_col_names:
                column_names = np.append(column_names,
                                         get_brightness_columns(num_centers))
    if return_col_names:
        return image_data, column_names
    else:
        return image_data
