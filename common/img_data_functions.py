"""A module with useful functions for manipulation of raw image data."""
from sklearn.feature_extraction import image
from scipy import misc
from skimage import exposure as ski_exposure, color as ski_color


def read_image(filename):
    """Read an image from the disk and output data arrays."""
    image_array_rgb = misc.imread(filename, mode='RGB')
    image_array_grey = misc.imread(filename, flatten=True, mode='F')
    image_array_luv = ski_color.rgb2luv()
    return image_array_rgb, image_array_grey, image_array_luv


def get_rgb_counts(rgb_image_array):
    """Ouput histographic arrays counting image RGB values."""
    red = rgb_image_array[:, :, 0].astype(int)
    green = rgb_image_array[:, :, 1].astype(int)
    blue = rgb_image_array[:, :, 2].astype(int)
    red = ski_exposure.histogram(red, nbins=256)
    green = ski_exposure.histogram(green, nbins=256)
    blue = ski_exposure.histogram(blue, nbins=256)
    return red, green, blue


def get_grey_counts(grey_image_array):
    """Output histographic array counting image greyscale values."""
    grey = grey_image_array.astype(int)
    grey = ski_exposure.histogram(grey, nbins=256)
    return grey


def get_luv_counts(luv_image_array):
    """Ouput histographic arrays counting image RGB values."""
    l = luv_image_array[:, :, 0].astype(int)
    u = luv_image_array[:, :, 1].astype(int)
    v = luv_image_array[:, :, 2].astype(int)
    l = ski_exposure.histogram(l, nbins=256)
    u = ski_exposure.histogram(u, nbins=256)
    v = ski_exposure.histogram(v, nbins=256)
    return l, u, v


def tril():
    return None
