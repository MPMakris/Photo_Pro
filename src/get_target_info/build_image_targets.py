"""A script for obtaining image target information from Flickr."""
import sys
from common.read_csv_files import read_image_feature_csv
from common.flicker_api_functions import get_user_data, get_image_data
import pandas as pd


def get_user_inputs(inputs):
    """Get user inputs from command line operation."""
    file_path = inputs[1]
    return file_path


def main(file_path):
    """
    The main function to run the script. Creates and saves a DataFrame.

    INPUTS:
    file_path | Image Feature CSV File Path (string)

    OUTPUTS:
    None
    """
    #  Get Picture Names and Owners:
    df_target = read_image_feature_csv(file_path, ['owner', 'id'])
    #  Get User Info from API:
    user_info = df_target['owner'].apply(get_user_data)
    user_info.columns = ['user_is_pro', 'user_can_buy_pro', 'user_total_views']
    df_target = pd.concat((df_target, user_info), axis=1)
    #  Get Image Info from API:
    image_info = df_target['id'].apply(get_image_data)
    image_info.columns = ['image_ncomments', 'image_nfavs', 'image_nsets',
                          'image_npools']
    df_target = pd.concat((df_target, image_info), axis=1)
    #  Save Target DataFrame to CSV
    save_name = file_path.replace('feature_data', 'target_data')
    pd.to_csv(save_name, header=True, index=True, index_label=False, mode='wb',
              encoding='utf-8', na_rep='NaN', sep='|')


if __name__ == "__main__":
    """
    Argv0: This File
    Argv1: Image Feature Filename
    """
    feature_info_file_path = get_user_inputs(sys.argv)
    main(feature_info_file_path)
