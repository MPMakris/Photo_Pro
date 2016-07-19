"""Saved methods for Flickr API use."""


def get_flickr_keys(filename='flickr.keys'):
    """Get the Ficker user and app keys from the .keys file."""
    keys_list = []
    flickr_keys = {}
    with open(filename) as f_open:
        for line in f_open:
            keys_list.append(line.strip('\n'))
    for key in keys_list:
        pair = key.split(":")
        flickr_keys[pair[0]] = pair[1]
    return flickr_keys
