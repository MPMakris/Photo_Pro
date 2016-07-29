"""A script to import images and build the data matrix for modeling."""
import sys
import numpy as np
import pandas as pd
from common.os_interaction import (get_files_in_folder,
                                   get_current_folder_name,
                                   check_folder_exists)
from read_image import ImageAnalyzer


def get_user_inputs(inputs):
    """Get user inputs from command line operation."""
    path = inputs[1]
    if path[-1] != "/":
        path += '/'
    if len(inputs) > 2:
        max_num_images = int(inputs[2])
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
                'discreet_nbins': {'rgb': 120, 'grey': 120, 'L': 50,
                                   'uv': 100},
                'medium_nbins': {'rgb': 30, 'grey': 30, 'L': 15,
                                 'uv': 25},
                'large_nbins': {'rgb': 12, 'grey': 12, 'L': 6,
                                'uv': 10},
                'channel_limits': {'rgb': (0, 255), 'grey': (0, 255),
                                   'L': (0, 100), 'uv': (-100, 100)},
                'create_max': True,
                'create_min': True,
                'create_mean': True,
                'create_median': True,
                'find_crispnesses': True,
                'find_aspect_ratio': True,
                'find_brightness_centers': True,
                'bright_centers_try': [3, 8]
                }
    return controls


def main(directory, max_num_images):
    """
    Run the main script for image feature creation.

    INPUTS:
    directory | Path to a source directory containing image files.
    max_num_images | Upper limit on number of images to anlayze. (Optional)

    OUPUTS:
    None | Creates a CSV file containing modeling feature data. Saves to:
           `data/modeling/[SEARCH_TERM]/`
    """
    image_names = get_files_in_folder(directory)
    feature_controls = set_feature_controls()
    print "\nBegin Processing {} Images:".format(
                                            get_current_folder_name(directory))
    if max_num_images is not None:
        print "Analyzing Maximum {} Images...".format(max_num_images)
        total = max_num_images
    else:
        print "Analyzing All Images in Directory..."
        total = len(image_names)
    # Begin Analyzing Images:
    for i, name in enumerate(image_names):
        image_path = directory + name
        if i == 0:
            image = ImageAnalyzer(image_path, feature_controls, True)
            image_data = image.feature_data
            column_names = image.column_names
        else:
            image = ImageAnalyzer(image_path, feature_controls, False)
            image_data = image.feature_data
        sys.stdout.write("Images Analyzed: {} of {}\r".format(i+1, total))
        sys.stdout.flush()
        if i == 0:
            all_data = list(image_data)
        else:
            all_data.append(image_data)
        if max_num_images is not None:
            if (i + 1) >= max_num_images:
                break
    all_data = np.array(all_data)
    print "\033[0;32mAnalysis COMPLETE\033[0m                            \n"
    # Create and Save Data Frame to CSV:
    print "Creating DataFrame..."
    df = pd.DataFrame(data=all_data, columns=column_names)
    dest_directory = ('data/modeling/' + get_current_folder_name(directory))
    check_folder_exists(dest_directory)
    dest_file = (dest_directory + '/feature_data' + '_' +
                 get_current_folder_name(directory) + '_' +
                 str(len(df)) + '.csv')
    df.to_csv(dest_file, sep='|', index=False)
    print "DataFrame Saved to:\n-->\033[1;36m{}\033[0m\n".format(dest_file)


if __name__ == "__main__":
    """
    Argv0: This File
    Argv1: Directory with Images
    Argv2: Max Number of Images to Read (Optional)
    """
    directory_path, max_num_images = get_user_inputs(sys.argv)
    main(directory_path, max_num_images)
