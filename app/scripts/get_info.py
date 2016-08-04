"""Functions for getting info that the server can display."""
from common.os_interaction import get_files_in_folder


def get_data_info(model_directory='scripts/data/store/',
                  image_directory='scripts/data/images/'):
    """Get info for the server to display correctly."""
    # Remember to add ../ before each directory
    file_names = get_files_in_folder(model_directory)
    model_names = []
    model_paths = []
    for name in file_names:
        if name.find('model') >= 0:
            model_names.append(name)
            model_paths.append(model_directory + name)

    image_directory = '../data/images/'
    folder_names = get_files_in_folder(image_directory)
    image_names = []
    image_paths = []
    for folder in folder_names:
        folder_name = image_directory + folder
        new_images = get_files_in_folder(folder_name)
        for image in new_images:
            image_path = folder_name + '/' + image
            image_paths.append(image_path)
        image_names.extend(new_images)

    num_models = len(model_names)
    num_images = len(image_names)
    return (num_images, num_models, image_names, image_paths, model_names,
            model_paths)
