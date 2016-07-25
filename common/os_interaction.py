"""Useful scripts for OS interaction."""
import os


def check_folder_exists(folder_name):
    """Check for folder; if it does not exist, creat it."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def get_file_name_from_path(file_path):
    """Reduce a file path down to just the file name without directories."""
    check = True
    while check:
        idx = file_path.find('/')
        if idx > 0:
            file_path = file_path[idx+1:]
        else:
            check = False
    return file_path


def get_files_in_folder(directory):
    """List the files in a directory."""
    return os.listdir(directory)
