"""A module for holding code to prepare image data for modeling."""
import pandas as pd
import cPickle as pickle
import math
from os_interaction import check_folder_exists
from sklearn.cross_validation import train_test_split
import copy.copy as copy
from sklearn.preprocessing import StandardScaler


def name_quantile_by_right(x, limits):
    """
    Name the quantile of the datapoint, starting at 1.

    PARAMETERS
    ----------
    x : numeric

    limits : list
        The right-side limits of the bins.
    """
    quantile_cats = range(1, len(limits)+1, 1)
    for cat, limit in zip(quantile_cats, limits):
        if x <= limit:
            return cat


def fit_transform_quantize_col(df_train, df_test, target_columns, col_name,
                               n_quantiles=5):
    """
    Fit and transform a new quantile target column.

    Create a new column in both DataFrames that quantizes a target column into
    equal size categories.

    PARAMETERS
    ----------
    df_train : pandas.DataFrame
        The training set data.

    df_test : pandas.DataFrame
        The testint set data.

    target_columns : list

    col_name : str

    n_quantiles : int
        The number of bins. For 4 bins (0 to 0.25, 0.25 to 0.5, etc...),
        n_quantiles=4.

    RETURNS
    -------
    df_train : pandas.DataFrame

    df_test : pandas.DataFrame

    target_columns : list

    limits : list (of floats)
        The outter limits of the quantiles.
    """
    min_value = math.floor(df_train[col_name].min())
    limits = []
    for i in range(1, n_quantiles+1):
        limits.append(math.ceil(df_train[col_name].quantile(
                                                        i/float(n_quantiles))))

    new_col_name = col_name+"_quantized"
    target_columns.append(new_col_name)

    data = df_train[col_name].apply(
                                lambda x: name_quantile_by_right(x, limits))
    df_train[new_col_name] = data
    df_test[new_col_name] = df_test[col_name].apply(
                                lambda x: name_quantile_by_right(x, limits))
    limits.insert(0, min_value)
    return df_train, df_test, target_columns, new_col_name, limits


def fit_transform_bin_col(df_train, df_test, target_columns, col_name,
                          bin_seps):
    """
    Fit and transform a new binned target column.

    Create a new column in both DataFrames that bins a target column by
    designated boundaries.

    PARAMETERS
    ----------
    df_train : pandas.DataFrame
        The training set data.

    df_test : pandas.DataFrame
        The testint set data.

    target_columns : list

    col_name : str

    bin_seps : list (of floats)
        The predicted outer dividing limits for bins. If max() and/or min() are
        outside these bins, they are added automatically.

    RETURNS
    -------
    df_train : pandas.DataFrame

    df_test : pandas.DataFrame

    target_columns : list

    bin_limits : list (of floats)
        Final outer bin limits list with max() or min() added as needed.
    """
    bin_seps = sorted(list(bin_seps))
    min_value = math.floor(df_train[col_name].min())
    max_value = math.ceil(df_train[col_name].max())

    if max_value > bin_seps[-1]:
        bin_seps.append(max_value)

    if min_value >= bin_seps[0]:
        trigger = True
        holder = bin_seps.pop(0)
    else:
        trigger = False

    new_col_name = col_name+"_binned"
    target_columns.append(new_col_name)

    df_train[new_col_name] = df_train[col_name].apply(
                                lambda x: name_quantile_by_right(x, bin_seps))
    df_test[new_col_name] = df_test[col_name].apply(
                                lambda x: name_quantile_by_right(x, bin_seps))
    if trigger:
        bin_seps.insert(0, holder)
    else:
        bin_seps.insert(0, min_value)

    return df_train, df_test, target_columns, new_col_name, bin_seps


def transform_col(df, col_name, bin_limits, transform_type):
    """
    Transform a target column on any new images into quantized or binned.

    PARAMETERS
    ----------
    df : pandas.DataFrame
        New observation(s).

    col_name : str
        Column to transform.

    bin_limits: list (of floats)

    transform_type : str
        Transform type of one of the following:

        - 'quantized'
        - 'binned'

    RETURNS
    -------
    df : pandas.DataFrame
        Observations with new transformed columns.
    """
    holder = bin_limits.pop(0)
    new_col_name = str(col_name) + "_" + str(transform_type)
    df[new_col_name] = df[col_name].apply(
                              lambda x: name_quantile_by_right(x, bin_limits))
    bin_limits.insert(0, holder)
    return df


def pop_columns(df, col_names):
    """
    Pop multiple columns off of a Pandas DataFrame.

    PARAMETERS
    ----------
    df : pandas.DataFrame

    col_names : list
        List of the columns to pop in order and append to new DataFrame.

    RETURNS
    -------
    df : pandas.DataFrame
        The orriginal DataFrame minus the popped columns.

    df_popped : pandas.DataFrame
        The popped columns in a new DataFrame.
    """
    df_copy = copy(df)
    for i, name in enumerate(list(col_names)):
        if i == 0:
            df_popped = df_copy.pop(name)
        else:
            df_popped = pd.concat((df_popped, df_copy.pop(name)), axis=1)
    return df_copy, df_popped


class data_prepper(object):
    """A class for prepping image data for modeling and for new images."""

    def __init__(self, df, target_columns, train_size=0.8, rand=42):
        """Init the image prepper."""
        self.column_limits = dict()
        self.target_columns = target_columns
        df_train, df_test = train_test_split(df, train_size=train_size,
                                             random_state=rand)
        self.df_train = df_train
        self.df_test = df_test
        self.train_size = train_size
        self.scaler = None
        self.scaler_run = False
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

    def fit_transform_quantile_col(self, column_name, n_quantiles):
        """Fit/transform a quantile column."""
        (self.df_train, self.df_test, self.target_columns, new_col_name,
            limits) = fit_transform_quantize_col(self.df_train, self.df_test,
                                                 self.target_columns,
                                                 column_name, n_quantiles=5)
        self.column_limits[new_col_name] = (limits, 'quantized')

    def fit_transform_binning_col(self, column_name, bin_limits):
        """Fit/transform a binning column."""
        (self.df_train, self.df_test, self.target_columns, new_col_name,
            limits) = fit_transform_bin_col(self.df_train, self.df_test,
                                            self.target_columns,
                                            column_name, bin_limits)
        self.column_limits[new_col_name] = (limits, 'binned')

    def transform_new_image_with_y(self, df):
        """
        Transform any new image observation(s) using existing stored limits.

        PARAMETERS:
        ----------
        df : pandas.DataFrame
            Complete observation info including features and target.

        RETURNS
        -------
        X, y : pandas.DataFrames
            Feature (X) and target (y) dataframes scalled and binned.
        """
        for column_name, value in self.column_limits.iteritems():
            (bin_limits, transform_type) = value
            df = transform_col(df, column_name, bin_limits, transform_type)
        X_new, y_new = pop_columns(df, self.target_columns)
        X_columns = X_new.columns
        X_new = self.scaler.transform(X_new)
        X_new = pd.DataFrame(data=X_new, columns=X_columns)
        return X_new, y_new

    def transform_new_image_without_y(self, X):
        """
        Transform any new image observation(s) according to the scaler.

        PARAMETERS:
        ----------
        X : pandas.DataFrame
            Feature (X) dataframe before scaling.

        RETURNS
        -------
        X: pandas.DataFrames
            Feature (X) dataframe after scaling.
        """
        X_columns = X.columns
        X_new = self.scaler.transform(X)
        X_new = pd.DataFrame(data=X_new, columns=X_columns)
        return X_new

    def save(self, folder_dest, filename):
        """Pickle this object at a location with the given name."""
        folder_dest = str(folder_dest)
        filename = str(filename)
        if folder_dest[-1] != '/':
            folder_dest = folder_dest + '/'
        check_folder_exists(folder_dest)
        with open(folder_dest + filename + '.pkl', 'w') as f:
            pickle.dump(self, f)

    def return_training_data(self):
        """Return X_train and y_train pandas.DataFrames."""
        if not self.scaler_run:
            self.fit_scaler_to_X_data()
        return self.X_train, self.y_train

    def return_testing_data(self):
        """Return X_test and y_test pandas.DataFrames."""
        if not self.scaler_run:
            self.fit_scaler_to_X_data()
        return self.X_test, self.y_test

    def fit_scaler_to_X_data(self):
        """Demean and Standardize Data, store the scaler."""
        #  Split into X, y:
        X_train, y_train = pop_columns(self.df_train, self.target_columns)
        X_test, y_test = pop_columns(self.df_train, self.target_columns)
        X_columns = X_train.columns
        #  Fit Training Data, Scale Training and Test:
        scaler_mean_std = StandardScaler()
        X_train = scaler_mean_std.fit_transform(X_train)
        X_test = scaler_mean_std.transform(X_test)
        X_train = pd.DataFrame(data=X_train, columns=X_columns)
        X_test = pd.DataFrame(data=X_test, columns=X_columns)
        self.scaler = scaler_mean_std
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.scaler_run = True
