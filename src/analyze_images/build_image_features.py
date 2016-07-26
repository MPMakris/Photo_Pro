"""A script to import images and build the data matrix for modeling."""
import sys
import numpy as np
import pandas as pd
from common.os_interaction import (get_files_in_folder,
                                   get_parent_directory_of_directory,
                                   get_current_folder_name,
                                   check_folder_exists)
from read_image import analyze_image


def get_user_inputs(inputs):
    """Get user inputs from command line operation."""
    path = inputs[1]
    if path[-1] != "/":
        path += '/'
    if len(inputs) > 2:
        max_num_images = inputs[2]
    else:
        max_num_images = None
    return path, max_num_images


def set_feature_controls():
    """Set controls for what features to create."""
    controls = {'enable_rgb': True,
                'enable_grey': True,
                'enable_luv': True,
                'discreet_bins': True,
                'medium_bins': True,
                'large_bins': True,
                'discreet_nbins': {'rgb': 255, 'grey': 255, 'l': 100,
                                   'uv': 200},
                'medium_nbins': {'rgb': 60, 'grey': 60, 'l': 20,
                                 'uv': 50},
                'large_nbins': {'rgb': 10, 'grey': 10, 'l': 6,
                                'uv': 12},
                'create_max': True,
                'create_min': True,
                'create_mean': True,
                'create_median': True
                }
    return controls


def compute_total_num_features(controls):
    """Precompute the total number of features for each image."""
    channel_keys = [key for key in controls.keys()
                    if key.find("enable") >= 0]
    feature_keys = [key for key in controls.keys()
                    if key.find("enable") < 0]
    features_per_channel = sum([controls[key] if key.find('bins') >= 0
                                else controls[key]*3 for key in feature_keys])
    num_channels = sum([controls[key]*1
                        if key.find("grey") >= 0 else controls[key]*3
                        for key in channel_keys])
    return features_per_channel*num_channels


def main(directory, max_num_images):
    """The main function for running the script."""
    image_names = get_files_in_folder(directory)
    feature_controls = set_feature_controls()
    total_features = compute_total_num_features(feature_controls)
    all_data = np.empty((0, total_features))
    print all_data.shape
    for i, name in enumerate(image_names):
        image_path = directory + name
        image_data, image_bin_centers = analyze_image(image_path,
                                                      feature_controls)
        print image_data.shape
        all_data = np.concatenate((all_data, image_data), axis=0)
        if max_num_images is not None:
            if i + 1 == max_num_images:
                break
    df = pd.DataFrame(data=all_data, index=image_names)

    save_directory = (get_parent_directory_of_directory(directory) +
                      'model_data/' + get_current_folder_name(directory))
    check_folder_exists(save_directory)
    df.to_csv(save_directory, sep='|', )


if __name__ == "__main__":
    """
    Argv0: This File
    Argv1: Directory with Images
    Argv2: Max Number of Images to Read (Optional)
    """
    directory_path, max_num_images = get_user_inputs(sys.argv)
    main(directory_path, max_num_images)
