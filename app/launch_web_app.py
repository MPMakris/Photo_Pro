#  -*- coding: utf-8 -*-
"""
    PhotoPro.Science

    A photography analytics project completed as a capstone for the Galvanize
    Data Science Immersive project.

    :copyright: (c) 2015 by Michael Makris.
    :license: BSD, see LICENSE for more details.
"""

from flask import (Flask, request, session, g, redirect, url_for, abort,
                   render_template, flash, Response)
from scripts.get_info import get_data_info
import pandas as pd
#  Creat the Applicaiton:
app = Flask(__name__)


#  Main Landing Page:
@app.route('/')
@app.route('/index')
def index():
    """Display the landing page."""
    return render_template('index.html')


@app.route('/analytics/<subpage>/')
def analytics(subpage='overview'):
    """Display the page: analytics/subpage."""
    return render_template('analytics/{}.html'.format(subpage))


@app.route('/graph')
def image_page():
    """Display the graph."""
    return render_template('../../notebooks/lines.html')


if __name__ == "__main__":
    print "Building References"
    (num_images, num_models, image_names, image_paths, model_names,
        model_paths) = get_data_info()
    app.run(host='0.0.0.0', port=8080, debug=True)
