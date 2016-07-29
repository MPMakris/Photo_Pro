"""A script for reading a single image and creating features."""
from common.img_data_functions import (read_image,
                                       find_aspect_ratio, calc_crispness,
                                       find_brightness_centers)
from common.os_interaction import get_file_name_from_path
from common.img_meta_functions import split_img_name
import numpy as np





def get_column_bin_names(controls, color, nbins):
    """
    Return the metric names to be included in the feature matrix.

    INPUTS:
    controls | The feature control dictionary.
    color | Name of the color the metric applies to (string).
    nbins | Number of bins for which the metric was calculated (int).

    OUPUTS:
    metric_names | A list of the metric names as strings.
    """
    column_bin_names = []
    column_bin_names.extend(["{}_bin{}_nbins{}".format(color, i, str(nbins))
                             for i in range(1, nbins+1)])

    if controls['create_max']:
        column_bin_names.append("{}_max_nbins{}".format(color, str(nbins)))
    if controls['create_min']:
        column_bin_names.append("{}_min_nbins{}".format(color, str(nbins)))
    if controls['create_mean']:
        column_bin_names.append("{}_mean_nbins{}".format(color, str(nbins)))
    if controls['create_median']:
        column_bin_names.append("{}_median_nbins{}".format(color, str(nbins)))
    return column_bin_names


def get_columns_for_bin_class(controls, bin_class):
    """
    Get column names for a class of bin size.

    INPUTS:
    controls | The feature control dictionary.
    bin_class | A string pointing to a bin class.

    OUTPUTS:
    bin_class_column_names | A list of column names for the channels called
                             in the bin class.
    """
    bin_class_column_names = []
    bin_class_alt = bin_class[:bin_class.find('_')] + "_nbins"
    if controls['enable_rgb']:
        for color in ['red', 'green', 'blue']:
            num_bins = controls[bin_class_alt]['rgb']
            bin_class_column_names = sum([bin_class_column_names,
                                          get_column_bin_names(controls,
                                                               color,
                                                               num_bins)], [])
    if controls['enable_grey']:
        for color in ['grey']:
            num_bins = controls[bin_class_alt]['grey']
            bin_class_column_names = sum([bin_class_column_names,
                                          get_column_bin_names(controls,
                                                               color,
                                                               num_bins)], [])
    if controls['enable_luv']:
        for color in ['l']:
            num_bins = controls[bin_class_alt]['l']
            bin_class_column_names = sum([bin_class_column_names,
                                          get_column_bin_names(controls,
                                                               color,
                                                               num_bins)], [])
    if controls['enable_luv']:
        for color in ['u', 'v']:
            num_bins = controls[bin_class_alt]['uv']
            bin_class_column_names = sum([bin_class_column_names,
                                          get_column_bin_names(controls,
                                                               color,
                                                               num_bins)], [])
    return bin_class_column_names


def get_brightness_columns(num_centers):
    """
    Get the list of column names for a given [num_centers].

    INPUTS:
    num_centers | The number of brightness centers determined (int).

    OUPUTS:
    center_column_names | A list of column names for brightness centers.
    """
    return ["bright_ctr{}_numctrs{}".format(i, num_centers)
            for i in range(1, num_centers+1)]


def extract_for_bin_size(image_array_rgb, image_array_grey, image_array_luv,
                         bin_class, controls):
    """
    Extract image channel features given a variable bin (nbins DICT) quantity.

    INPUTS:
    image_array_rgb | A 3D Numpy array of of the RGB image data.
    image_array_grey | A 2D Numpy array of of the Greyscale image data.
    image_array_luv | A 3D Numpy array of of the LUV image data.
    nbins | A Dictionary of nbin values, with the channel type as the key.
            Example: nbins = {'rgb': 255, 'grey': 255, 'l': 100, 'uv': 200}
    controls | A Dictionary containing feature control information.

    OUTPUTS:
    image_feature_data | A list of all the concatenated feature data.
    """
    bin_class_alt = bin_class[:bin_class.find('_')] + "_nbins"
    nbins = controls[bin_class_alt]
    # Set Up Empty Array for Incoming Feature Data:
    image_feature_data = []
    # Extract Image Feature Data
    if controls['enable_rgb']:
        num_bins = nbins['rgb']
        red_counts, red_metrics = get_channel_data(image_array_rgb[:, :, 0],
                                                   0, 255, num_bins)
        green_counts, green_metrics = get_channel_data(image_array_rgb[:, :, 1],
                                                       0, 255, num_bins)
        blue_counts, blue_metrics = get_channel_data(image_array_rgb[:, :, 2],
                                                     0, 255, num_bins)
        rgb_features = sum([red_counts,
                            filter_metrics(red_metrics, controls),
                            green_counts,
                            filter_metrics(green_metrics, controls),
                            blue_counts,
                            filter_metrics(blue_metrics, controls)], [])
        image_feature_data = sum([image_feature_data, rgb_features], [])
        # print "AFTER RGB: {}".format(image_feature_data.shape)
    if controls['enable_grey']:
        num_bins = nbins['grey']
        grey_counts, grey_metrics = get_channel_data(image_array_grey, 0, 255,
                                                     num_bins)
        grey_features = sum([grey_counts,
                             filter_metrics(grey_metrics, controls)], [])
        image_feature_data = sum([image_feature_data, grey_features], [])
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
        luv_features = sum([l_counts,
                            filter_metrics(l_metrics, controls),
                            u_counts,
                            filter_metrics(u_metrics, controls),
                            v_counts,
                            filter_metrics(v_metrics, controls)], [])
        image_feature_data = sum([image_feature_data, luv_features], [])
    #     print "AFTER LUV: {}".format(image_feature_data.shape)
    # print "TOTAL AFTER BIN SIZE RUN: {}".format(image_feature_data.shape)
    return image_feature_data


def analyze_image(image_path, controls, return_col_names=False):
    """
    Produce the total feature row data for a single image.

    INPUTS:
    image_path | String representation of image location on disk.
    controls | A Dictionary containing feature control information.
    q | FOR PARALLEL PROCESSING
    return_col_names | A boolean input that controls if the function outputs
                       column names list. (optional)

    OUTPUT:
    image_data | A list of all the concatenated feature data.
    column_names | A list of all the column names (conditional on inputs).
    """
    # Get File Owner and ID Fields:
    image_name = get_file_name_from_path(image_path)
    owner, ID = split_img_name(image_name)
    # Prep Array to Hold data
    image_data = [owner, ID]
    column_names = ['owner', 'id']
    # Read in Raw Image Channel Arrays
    image_array_rgb, image_array_grey, image_array_luv = read_image(image_path)
    # Get Featurized Data from Raw Image Channel Arrays
    for bin_class in ['discreet_bins', 'medium_bins', 'large_bins']:
        if controls[bin_class]:
            image_data = sum([image_data,
                              extract_for_bin_size(image_array_rgb,
                                                   image_array_grey,
                                                   image_array_luv,
                                                   bin_class,
                                                   controls)], [])
            if return_col_names:
                column_names = sum([column_names,
                                    get_columns_for_bin_class(controls,
                                                              bin_class)], [])
    if controls['find_crispnesses']:
        image_data.extend(calc_crispness(image_array_grey))
        if return_col_names:
            column_names.extend(['crisp_sobel', 'crisp_canny', 'script'])
    if controls['find_aspect_ratio']:
        image_data.append(find_aspect_ratio(image_array_grey))
        if return_col_names:
            column_names.append('aspect_ratio')
    if controls['find_brightness_centers']:
        for num_centers in controls['bright_centers_try']:
            image_data.extend(find_brightness_centers(image_array_grey,
                                                      num_centers))
            if return_col_names:
                column_names.extend(get_brightness_columns(num_centers))
    #  q.put(image_data)

    if return_col_names:
        return image_data, column_names
    else:
        return image_data
        #  queue.put(image_data)


class ImageAnalyzer(object):
    """An ImageAnalyzer extracting feature information from an image.

    Written for parallelization using Python's parallel processing.

    PARAMETERS
    ----------
    image_path : str
        Location of the image to analyze.

    f_controls : dict
        Dictionary passed to :class:`ImageAnalyzer` conrolling which feature
        is information created.

    columns_out : boolean, optional (default = False)
        Optional input to produce a list of the feature names.
    """

    def __init__(self, image_path, f_controls, columns_out=False):

        self.image_path = image_path
        self.image_name = get_file_name_from_path(image_path)
        self.rgb_raw, self.grey_raw, self.luv_raw = read_image(image_path)
        self.controls = f_controls
        self.feature_data = []
        self.column_names = []

    def get_features(self):
        """Put called commands in order here."""
        return

    def _featurize_channel(self, channel_raw, channel_name, channel_class,
                           bin_class):
        """Featurizes a single channel.

        PARAMETERS
        ----------
        channel_raw : 2D numpy array

        channel_name : str

        channel_class : str
            Class of channel data, determines the range of possible values.

            - 'rgb' : red, green, blue
            - 'grey' : greyscale
            - 'l' : luminance
            - 'uv' : chromaticity

        bin_class : str
            Bin scales determing the number of bins created.

            - discreet : finest binning
            - medium : medium binning
            - large : largest binning
        """
        bin_key = bin_class + "_nbins"
        nbins = self.controls[bin_key][channel_class]
        lower, upper = self.controls['channel_limits'][channel_class]

        counts, metrics = self._get_channel_data(channel_raw, lower, upper,
                                                 nbins)
        metrics = self._filter_metrics(metrics)

        self.feature_data.append(counts)
        if self.controls['']:
            self.column_names['']

    def _get_channel_data(self, image_array, lower, upper, nbins):
        """Get channel feature data.

        PARAMETERS
        ----------
        image_array : 2D numpy array
            Raw data for a single channel.

        lower : int
            Lower limit of channel data values allowed.

        upper : int
            Upper limit of channel data values allowed.

        nbins : int
            Number of bins to put data into.

        RETURNS
        -------
        counts : list
            A list of the counts of channel values in each bin.

        metrics : list of floats (max, min, mean, median)
            A list of the metrics for the channel, filtered by the control
            dictionary ``f_control``.
        """
        values = image_array.astype(int).flatten()
        data = np.round(values, decimals=0).astype(float)
        bin_width = ((upper+1) - lower)/float(nbins)
        steps = np.arange(lower, upper+1+bin_width, bin_width)[0:nbins+1]
        hist, edges = np.histogram(data, bins=steps, density=True)
        counts = list(hist)
        metrics = sum([[m for m in [values.max()]
                        if self.controls['create_max']],
                       [m for m in [values.min()]
                       if self.controls['create_min']],
                       [m for m in [np.mean(values)]
                       if self.controls['create_mean']],
                       [m for m in [np.median(values)]
                       if self.controls['create_median']]], [])
        return counts, metrics
