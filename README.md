## [PhotoPro](<http://photopro.science>)
An intelligent photo analysis tool for making predictions on Flickr views and professional status of the photographer.

#### Summary
**PhotoPro** is meant to help you pick better photos. Whether you are a marketer, professional photographer, or social media enthusiast, getting your photos online is an integral part of your business and/or identity.

Choosing the best photos to attract attention is often a matter of opinion. While it might be easy to identify the wrong photo, choosing the right photo that makes uses *want* to look at your ad is tough.

**PhotoPro** can help guide that decision. Trained on over 100,000 images from Flickr, it can predict with high precision and recall where on a distribution of past performance metrics your photo will perform, based only on the appearance of the photo.

### Dependencies
<img src="app/static/index/img/python_icon.png" height="100"/>
<img src="app/static/index/img/anaconda_icon.png" height="100"/>
<img src="app/static/index/img/ipython_icon.png" height="100"/>
<img src="app/static/index/img/sklearn_icon.png" height="100"/>
<img src="app/static/index/img/graphlab_icon.png" height="100"/>
<img src="app/static/index/img/scikit-image_icon.png" height="100"/>
<img src="app/static/index/img/flask_icon.png" height="100"/>
<img src="app/static/index/img/jinja2_icon.png" height="100"/>
<img src="app/static/index/img/bootstrap_icon.png" height="100"/>
<img src="app/static/index/img/flot_icon.png" height="100"/>
* [Python](<https://www.python.org/>)
* [Anaconda](<https://www.continuum.io/why-anaconda>)
* [iPython](<https://ipython.org/>)
* [Numpy](<http://www.numpy.org/>)
* [Pandas](<http://pandas.pydata.org/>)
* [SKLearn](<http://scikit-learn.org/>)
* [Graphlab by Turi (previously Dato)](<https://turi.com/>)
* [Scikit-Image](<http://scikit-image.org/>)
* [SciPy](<https://www.scipy.org/>)
* [Flask](<http://flask.pocoo.org/>)
* [Jinja2](<http://jinja.pocoo.org/>)
* [Start Bootstrap](<https://startbootstrap.com/>)
* [Flot](<http://www.flotcharts.org/>)
* [Beautiful Soup](<https://www.crummy.com/software/BeautifulSoup/>)

#### Data Acquisition
Data for the project is obtained from the Flickr API. Starting with a keyword, meta data for the requested images is downloaded and stored in .CSV files. Next, the raw image files are downloaded and stored.

###### Search for a Keyword
Start your search with a [keyword] like `landscape`. It is recommended to also indicate a maximum number of pages to download, [max_pages]. Each page contains information for 500 pictures. If [max_pages] is not provided, the resulting data download may be excessive.

Run the following code in the command line:
```
python src/source/search_save_pictures_meta.py [keyword] [max_pages]
```

The meta data downloaded from the indicated search is saved in a .CSV file called `data/tables/flickr_image_search_for_[KEYWORD]_[max_pages].csv`.

###### Download Images

#### Exploratory Data analysis

###### Target selection

#### Feature Engineering
#### Acknowledgements
http://stackoverflow.com/questions/1994037/flickr-api-returning-duplicate-photos
requests library
beautiful soup library
