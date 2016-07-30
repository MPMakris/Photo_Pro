"""A script to import images and build the data matrix for modeling."""
import sys
import os
import numpy as np
import pandas as pd
from common.os_interaction import get_files_in_folder, get_current_folder_name, check_folder_exists
from read_image import ImageFeaturizer
from multiprocessing import Process, Queue


def get_user_inputs(inputs):
    """Get user inputs from command line operation."""
    path = inputs[1]
    if path[-1] != "/":
        path += '/'
    n_processes = int(inputs[2])
    if len(inputs) > 3:
        max_num_images = int(inputs[3])
    else:
        max_num_images = None
    return path, n_processes, max_num_images


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


def analyze_images(directory, path_names, controls, fqueue):
    """Instaniate a single ImageAnalyzer object and store features."""
    for path in list(path_names):
        image = ImageFeaturizer(directory+path, controls, False)
        fqueue.put(image.feature_data)


def get_names(path_name, controls, boo):
    """Instantiate the first ImageAnalyzer and return features and names."""
    image = ImageFeaturizer(path_name, controls, boo)
    return image.feature_data, image.column_names


def main(directory, max_num_images, n_processes):
    """
    Run the main script for image feature creation.

    INPUTS:
    directory | Path to a source directory containing image files.
    max_num_images | Upper limit on number of images to anlayze. (Optional)

    OUPUTS:
    None | Creates a CSV file containing modeling feature data. Saves to:
           `data/modeling/[SEARCH_TERM]/`
    """
    image_names = get_files_in_folder(directory)[:max_num_images]
    feature_controls = set_feature_controls()
    print "\nBegin Processing {} Images:".format(
                                            get_current_folder_name(directory))
    if max_num_images is not None:
        print "Analyzing Maximum {} Images...\n".format(max_num_images)
    else:
        print "Analyzing Approx. All Images in Directory...\n"
    # Begin Analyzing Images:
    fqueue = Queue()
    processes = []
    #  Analyze First Image and Get Column Names:
    sys.stdout.write("Analyzing First Image and Creating Feature Names\n\n")
    sys.stdout.flush()
    features_1, column_names = get_names(directory+image_names[0],
                                         feature_controls, True)
    #  Organize Remaining Images into
    sys.stdout.write("Begin Multiprocessing Images:\n")
    sys.stdout.flush()
    remaining_names = np.array(image_names[1:])
    idx = len(remaining_names) % n_processes
    if idx == 0:
        image_paths_lists = np.split(remaining_names, n_processes)
    else:
        image_paths_lists = np.split(remaining_names[:-idx], n_processes)

    for path_list in image_paths_lists:
        processes.append(Process(target=analyze_images,
                                 args=(directory, path_list, feature_controls,
                                       fqueue, )))
    for t in processes:
        t.start()
    features = [features_1]
    #  Check that all Processes are Alive:
    while sum([a.is_alive() for a in processes]) != n_processes:
        sys.stdout.write("\rLiving Processes: {}".format(
                                      sum([a.is_alive() for a in processes])))
        sys.stdout.flush()
    sys.stdout.write("\rLiving Processes: {}\n".format(len(processes)))
    sys.stdout.flush()
    #  Loop Through Queue Until All Processes Complete and Die:
    check = True
    while check:
        if sum([a.is_alive() for a in processes]) == 0:
            check = False
        try:
            features.append(fqueue.get(block=True, timeout=2))
        except:
            pass
        sys.stdout.write(
                "\rLooping... \033[0;32m{} Images Analyzed\033[0m".format(
                                                               len(features)))
        sys.stdout.flush()
    sys.stdout.write(
        "\r\033[0;32mANALYSIS COMPLETE\033[0m for {} Directory    \n\n".format(
                                          get_current_folder_name(directory)))
    sys.stdout.flush()

    # for i, name in enumerate(image_names):
    #     image_path = directory + name
    #     if i == 0:
    #         image = ImageFeaturizer(image_path, feature_controls, True)
    #         image_data = image.feature_data
    #         column_names = image.column_names
    #     else:
    #         image = ImageFeaturizer(image_path, feature_controls, False)
    #         image_data = image.feature_data
    #     sys.stdout.write("Images Analyzed: {} of {}\r".format(i+1, total))
    #     sys.stdout.flush()
    #     if i == 0:
    #         all_data = list(image_data)
    #     else:
    #         all_data.append(image_data)
    #     if max_num_images is not None:
    #         if (i + 1) >= max_num_images:
    #             break

    # Create and Save Data Frame to CSV:
    print "Creating DataFrame..."
    df = pd.DataFrame(data=np.array(features), columns=column_names)
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
    Argv2: Number of Parallel Processes to Run
    Argv3: Max Number of Images to Read (Optional)
    """
    directory_path, n_processes, max_num_images = get_user_inputs(sys.argv)
    main(directory_path, max_num_images, n_processes)
