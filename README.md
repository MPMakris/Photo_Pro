# Photo_Pro
A photo editing and stylizing tool built from neural networks.

### Data Acquisition Pipeline
Data for the project is obtained from the Flickr API. Starting with a keyword, meta data for the requested images is downloaded and stored in .CSV files. Next, the raw image files are downloaded and stored.

##### Search for a Keyword
Start your search with a [keyword] like `landscape`. It is recommended to also indicate a maximum number of pages to download, [max_pages]. Each page contains information for 500 pictures. If [max_pages] is not provided, the resulting data download may be excessive.

Run the following code in the command line:
```
python src/source/search_save_pictures_meta.py [keyword] [max_pages]
```

The meta data downloaded from the indicated search is saved in a .CSV file called `data/tables/flickr_image_search_for_[KEYWORD]_[max_pages].csv`.

##### Download Images
