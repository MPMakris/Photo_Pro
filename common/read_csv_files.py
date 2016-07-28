"""A module for standarding the reading of CSV files saved for this project."""
import pandas as pd


def read_image_meta_csv(file_path, column_names_to_keep=None):
    """
    Read image meta data CSV into a Pandas DataFrame.

    INPUTS:
    filename | CSV file path to read. (string)

    OUTPUTS:
    df_meta | A Pandas DataFrame of the image meta data.
    """
    df_meta = pd.read_csv(file_path, sep='|')
    if column_names_to_keep is None:
        return df_meta
    else:
        df_meta[column_names_to_keep]


def read_image_feature_csv(file_path, column_names_to_keep=None):
    """
    Read image feature data CSV into a Pandas DataFrame.

    INPUTS:
    filename | CSV file path to read. (string)
    column_names_to_keep | A list of the columns to keep. Drop all others.
                           (python list)

    OUTPUTS:
    df_feature | A Pandas DataFrame of the image feature data.
    """
    df_feature = pd.read_csv(file_path, sep='|', index_col=None)
    if column_names_to_keep is None:
        return df_feature
    else:
        df_feature[column_names_to_keep]


def read_image_target_csv(file_path, column_names_to_keep=None):
    """
    Read image target data CSV into a Pandas DataFrame.

    INPUTS:
    filename | CSV file path to read. (string)

    OUTPUTS:
    df_target | A Pandas DataFrame of the image target data.
    """
    df_target = pd.read_csv(file_path, sep='|')
    if column_names_to_keep is None:
        return df_target
    else:
        df_target[column_names_to_keep]
