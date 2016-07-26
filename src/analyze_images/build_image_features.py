"""A script to import images and build the data matrix for modeling."""
import sys
import numpy as np
from common.os_interaction import get_files_in_folder
from read_image import analyze_image


def get_user_inputs(inputs):
    """Get user inputs from command line operation."""
    path = inputs[1]
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
                'discreet_bins': 256,
                'medium_bins': 32,
                'large_bins': 8,
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
    features_per_channel = sum([controls[key] for key in feature_keys])
    num_channels = sum([controls[key]*1
                        if key.find("grey") >= 0 else controls[key]*3
                        for key in channel_keys])
    return features_per_channel*num_channels, features_per_channel


def main(directory, max_num_images):
    """The main function for running the script."""
    image_names = get_files_in_folder(directory)
    feature_controls = set_feature_controls()
    total_features, features_per_channel = compute_total_num_features(feature_controls)
    data = np.empty((0, total_features))
    for i, name in enumerate(image_names):
        image_path = directory + name
        if i == 0:
            return_names = True
        else:
            return_names = False
        image_data = analyze_image(image_path, feature_controls, total_features, features_per_channel, return_names)
        data.append(image_data)
    return None


if __name__ == "__main__":
    """
    Argv0: This File
    Argv1: Directory with Images
    Argv2: Max Number of Images to Read (Optional)
    """
    directory_path, max_num_images = get_user_inputs(sys.argv)
    main(directory_path, max_num_images)
