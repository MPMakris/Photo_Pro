"""Functions for getting info that the server can display."""
from common.os_interaction import get_files_in_folder
import pandas as pd
import numpy as np
from common.img_data_functions import custom_hist
import cPickle as pickle
import os
import pdb


def open_model(file_path):
    """Open the DataPrepper from pickled file."""
    with open(file_path) as f:
        model = pickle.load(f)
    return model


def get_overview_info(model_directory='/home/ubuntu/efs/GIT/Photo_Pro/data/store/',
                      image_directory='/home/ubuntu/efs/GIT/Photo_Pro/data/images/'):
    """Get info for the server to display correctly."""
    # Remember to add ../ before each directory
    # pdb.set_trace()
    file_names = get_files_in_folder(model_directory)
    model_names = []
    model_paths = []
    for name in file_names:
        if ((name.find('model') >= 0) and (name.find('plot') >= 0)):
            model_names.append(name)
            model_paths.append(model_directory + name)

    # image_directory = '/home/ubuntu/efs/GIT/Photo_Pro/app/data/images/'
    folder_names = os.listdir(image_directory)
    # pdb.set_trace()
    image_names = []
    image_paths = []
    for folder in folder_names:
        folder_name = image_directory + folder
        print folder_name
        new_images = os.listdir(folder_name)
        for image in new_images:
            image_path = 'data/images/' + folder + '/' + image
            image_paths.append(image_path)
        # pdb.set_trace()
        image_names.extend(new_images)
    # pdb.set_trace()
    num_models = len(model_names)
    num_images = len(image_names)
    # pdb.set_trace()
    return (num_images, num_models, image_names, image_paths, model_names,
            model_paths)


def read_user_and_image_views(prepper):
    """Read in All Data."""
    X_train, y_train = prepper.return_training_data()
    X_test, y_test = prepper.return_testing_data()
    X_combined = pd.concat((X_train, X_test), axis=0)
    y_combined = pd.concat((y_train, y_test), axis=0)
    #  Get Views Per Owner Counts:
    ownwer_views = np.array(list(y_combined[['user_total_views']].groupby(
                                                      level=0).mean().values))
    owner_counts = custom_hist(ownwer_views, 0, 1000, 1000, density=False)
    owner_data = []
    for i, count in enumerate(owner_counts):
        owner_data.append([i, count])
    #  Get Views Per Image Counts:
    image_views = np.array(list(y_combined[['image_views']].values))
    image_counts = custom_hist(image_views, 0, 1000, 1000, density=False)
    image_data = []
    for i, count in enumerate(image_counts):
        image_data.append([i, count])
    pro_counts = y_combined['user_is_pro'].value_counts(ascending=True)
    pro_data = [[0, pro_counts[0]],
                [1, pro_counts[1]]]
    return image_data, owner_data, pro_data, X_combined, y_combined
