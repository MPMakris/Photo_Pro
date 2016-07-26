"""A module with useful functions for image meta data."""


def split_img_name(name):
    """Split image file name into Owner and ID strings."""
    parts = name.split('_')
    second = parts[1].split('.')
    return parts[0], second[0]


def pull_image_meta_info(df, owner, id_num):
    """Get Owner and ID numbers from meta DataFrame."""
    sub_df = df[df['owner'] == str(owner)]
    sub_df = sub_df[sub_df['id'] == int(id_num)]
    return int(sub_df['views'])
