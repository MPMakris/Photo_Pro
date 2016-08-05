"""Functions for getting info that the server can display."""
from common.os_interaction import get_files_in_folder
import pandas as pd
import numpy as np
from common.img_data_functions import custom_hist


def get_overview_info(model_directory='scripts/data/store/',
                      image_directory='scripts/data/images/'):
    """Get info for the server to display correctly."""
    # Remember to add ../ before each directory
    file_names = get_files_in_folder(model_directory)
    model_names = []
    model_paths = []
    for name in file_names:
        if ((name.find('model') >= 0) and (name.find('plot') >= 0)):
            model_names.append(name)
            model_paths.append(model_directory + name)

    image_directory = 'scripts/data/images/'
    folder_names = get_files_in_folder(image_directory)
    image_names = []
    image_paths = []
    for folder in folder_names:
        folder_name = 'data/images/' + folder
        new_images = get_files_in_folder(folder_name)
        for image in new_images:
            image_path = folder_name + '/' + image
            image_paths.append(image_path)
        image_names.extend(new_images)

    num_models = len(model_names)
    num_images = len(image_names)
    return (num_images, num_models, image_names, image_paths, model_names,
            model_paths)


def read_user_and_image_views(prepper):
    """Read in All Data."""
    X_train, y_train = prepper.return_training_data()
    X_test, y_test = prepper.return_testing_data()
    y_combined = pd.concat((y_train, y_test), axis=0)
    #  Get Views Per Owner Counts:
    ownwer_views = np.array(list(y_combined[['user_total_views']].groupby(level=0).mean().values))
    owner_counts = custom_hist(ownwer_views, 0, 1000, 1000)
    owner_data = []
    for i, count in enumerate(owner_counts):
        owner_data.append([i, count])
    #  Get Views Per Image Counts:
    image_views = np.array(list(y_combined[['image_views']].groupby(level=0).mean().values))
    image_counts = custom_hist(image_views, 0, 1000, 1000)
    image_data = []
    for i, count in enumerate(image_counts):
        image_data.append([i, count])
    pro_counts = y_combined['user_is_pro'].value_counts(ascending=True)
    pro_data = [{"label": "Non-Pro", "data": pro_counts[0]},
                {"label": "Pro", "data": pro_counts[1]}]
    return image_data, owner_data, pro_data
