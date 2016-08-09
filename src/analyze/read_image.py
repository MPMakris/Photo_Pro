"""A script for reading a single image and creating features."""
from common.img_data_functions import read_image, custom_hist
from common.os_interaction import get_file_name_from_path
from common.img_meta_functions import split_img_name
import numpy as np
from skimage import filters, feature
from sklearn.cluster import KMeans


class ImageFeaturizer(object):
    """An ImageFeaturizer extracting feature information from an image.

    Written for parallelization using Python's parallel processing.

    PARAMETERS
    ----------
    image_path : str
        Location of the image to analyze.

    f_controls : dict
        Dictionary passed to :class:`ImageFeaturizer` conrolling which feature
        is information created.

    columns_out : boolean, optional (default = False)
        Optional input to produce a list of the feature names.
    """

    def __init__(self, image_path, f_controls, columns_out=False):
        """Initialize the object."""
        self.image_path = image_path
        self.controls = f_controls
        self.columns_out = columns_out

        self.image_name = get_file_name_from_path(image_path)
        self.rgb_raw, self.grey_raw, self.luv_raw = read_image(image_path)

        self.feature_data = []
        self.column_names = []

        self._get_features()

    def _get_features(self):
        """Put called commands in order here."""
        self.feature_data.extend(split_img_name(self.image_name))
        self.column_names.extend(['owner', 'id'])
        for bin_class in ['discreet', 'medium', 'large']:
            if self.controls['enable_rgb']:
                self._featurize_channel(self.rgb_raw[:, :, 0], 'red', 'rgb',
                                        bin_class)
                self._featurize_channel(self.rgb_raw[:, :, 1], 'green', 'rgb',
                                        bin_class)
                self._featurize_channel(self.rgb_raw[:, :, 2], 'blue', 'rgb',
                                        bin_class)
                self._featurize_channel(self.grey_raw, 'red', 'rgb',
                                        bin_class)
                self._featurize_channel(self.luv_raw[:, :, 0], 'L', 'L',
                                        bin_class)
                self._featurize_channel(self.luv_raw[:, :, 1], 'v', 'uv',
                                        bin_class)
                self._featurize_channel(self.luv_raw[:, :, 2], 'u', 'uv',
                                        bin_class)
        if self.controls['find_crispnesses']:
            self._calc_crispness(self.grey_raw)
        if self.controls['find_aspect_ratio']:
            self._calc_aspect_ratio(self.grey_raw)
        if self.controls['find_brightness_centers']:
            for num_centers in self.controls['bright_centers_try']:
                self._calc_brightness_centers(self.grey_raw, num_centers)

    def _featurize_channel(self, channel_raw, channel_name, channel_class,
                           bin_class):
        """Featurize a single channel.

        PARAMETERS
        ----------
        channel_raw : 2D numpy array

        channel_name : str
            Name of channel.

            - red, green, blue, grey, L, u, or v

        channel_class : str
            Class of channel data, determines the range of possible values.

            - rgb : red, green, blue
            - grey : greyscale
            - L : luminance
            - uv : chromaticity

        bin_class : str
            Bin scales determing the number of bins created.

            - discreet : finest binning
            - medium : medium binning
            - large : largest binning
        """
        bin_key = bin_class + "_nbins"
        nbins = self.controls[bin_key][channel_class]
        lower, upper = self.controls['channel_limits'][channel_class]
        #  Get Feature Data:
        counts, metrics = self._get_channel_data(channel_raw, lower, upper,
                                                 nbins)
        self.feature_data.extend(counts+metrics)
        # Get Column Names:
        if self.columns_out:
            self.column_names.extend(self._get_channel_column_names(
                                                        channel_name, nbins))

    def _get_channel_data(self, channel_array, lower, upper, nbins):
        """Get channel feature data.

        PARAMETERS
        ----------
        channel_array : 2D numpy array
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
        values = channel_array.astype(int).flatten()
        data = np.round(values, decimals=0).astype(float)
        bin_width = ((upper+1) - lower)/float(nbins)
        steps = np.arange(lower, upper+1+bin_width, bin_width)[0:nbins+1]
        hist, edges = np.histogram(data, bins=steps, density=True)
        metrics = sum([[m for m in [values.max()]
                        if self.controls['create_max']],
                       [m for m in [values.min()]
                       if self.controls['create_min']],
                       [m for m in [np.mean(values)]
                       if self.controls['create_mean']],
                       [m for m in [np.median(values)]
                       if self.controls['create_median']]], [])
        return list(hist), metrics

    def _get_channel_column_names(self, channel_name, nbins):
        """
        Return the metric names to be included in the feature matrix.

        PARAMETERS
        ----------
        channel_name : str
            Name of channel.

            - red, green, blue, grey, L, u, or v

        nbins : ints
            Number of bins into which the channel values were counted.

        RETURNS
        -------
        channel_column_names : list
            A list of the channel's feature names.
        """
        channel_column_names = []
        channel_column_names.extend(["{}_bin{}_nbins{}".format(
                                                  channel_name, i, str(nbins))
                                     for i in range(1, nbins+1)])

        if self.controls['create_max']:
            channel_column_names.append("{}_max_nbins{}".format(channel_name,
                                                                str(nbins)))
        if self.controls['create_min']:
            channel_column_names.append("{}_min_nbins{}".format(channel_name,
                                                                str(nbins)))
        if self.controls['create_mean']:
            channel_column_names.append("{}_mean_nbins{}".format(channel_name,
                                                                 str(nbins)))
        if self.controls['create_median']:
            channel_column_names.append("{}_median_nbins{}".format(
                                                    channel_name, str(nbins)))
        return channel_column_names

    def _calc_crispness(self, grey_array):
        """Calculate three measures of the crispness of an channel.

        PARAMETERS
        ----------
        grey_array : 2D numpy array
            Raw data for the grey channel.

        PRODUCES
        --------
        crispnesses : list
            Three measures of the crispness in the grey channel of types:

            - ``sobel``, ``canny``, and ``laplace``
        """
        grey_array = grey_array/255
        sobel_var = filters.sobel(grey_array).var()
        canny_array = feature.canny(grey_array, sigma=1).var()
        canny_ratio = np.sum(canny_array == True)/float(
                                                    len(canny_array.flatten()))
        laplace_var = filters.laplace(grey_array, ksize=3).var()
        self.feature_data.extend([sobel_var, canny_ratio, laplace_var])
        if self.columns_out:
            self.column_names.extend(['crisp_sobel', 'crisp_canny',
                                      'crisp_laplace'])

    def _calc_aspect_ratio(self, channel_array):
        """Find the aspect ratio of an image.

        PARAMETERS
        ----------
        channel_array : 2D numpy array
            Raw data for a single channel.

        PRODUCES
        --------
        ratio : float
            The aspect ratio of the image.
        """
        self.feature_data.append(channel_array.shape[1]/float(
                                                      channel_array.shape[0]))
        if self.columns_out:
            self.column_names.append('aspect_ratio')

    def _calc_brightness_centers(self, grey_array, num_centers=3):
        """Find brightness centers in an immage using KMeans cluter.

        PARAMETERS
        ----------
        grey_array : 2D numpy array
            Raw data for a the grey channel.

        num_centers : int
            Number of brightness centers to return.

        PRODUCES
        --------
        centers : list
            The dominant brightness cluster center values in sorted order.
        """
        X = grey_array.flatten().reshape((-1, 1))
        model = KMeans(n_clusters=num_centers, n_jobs=1, n_init=4,
                       random_state=42)
        model.fit(X)
        centers = model.cluster_centers_.reshape((-1, ))
        counts = custom_hist(model.labels_, 0, num_centers-1, num_centers)
        self.feature_data.extend(list(centers[np.argsort(counts)[::-1]]))
        if self.columns_out:
            self.column_names.extend(
                            ["bright_ctr{}_numctrs{}".format(i, num_centers)
                             for i in range(1, num_centers+1)])
