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
from scripts.common.data_preparation import open_prepper
from scripts.get_info import read_user_and_image_views
from scripts.get_info import get_overview_info
import pandas as pd
import numpy as np

import pdb
#  Creat the Applicaiton:
app = Flask(__name__)


#  Main Landing Page:
@app.route('/')
@app.route('/index')
def index():
    """Display the landing page."""
    return render_template('index.html')


@app.route('/analytics/overview')
def analytics():
    """Display the page: analytics/overview."""
    return render_template('analytics/overview.html')


@app.route('/overview')
def overview():
    """Show the Overview page."""
    image_views, user_total_views = read_user_and_image_views()
    return render_template('analytics/overview.html', image_views=image_data,
                           user_total_views=owner_data,
                           user_is_pro=pro_data)


@app.route('/analyze_photo')
def analyze_photo():
    """Show Analyze Photo page."""
    return render_template('analytics/analyze_photo.html')


@app.route('/previous_results')
def previous_results():
    """Show previous results page."""
    return render_template('analytics/previous_results.html')


@app.route('/test')
def test_page():
    """Display the graph."""
    return render_template('test.html')


if __name__ == "__main__":
    try:
        print "Building References"
        (num_images, num_models, image_names, image_paths, model_names,
            model_paths) = get_overview_info()
    except:
        pass
    pdb.set_trace()
    all_images_prepper = open_prepper(
                         '/home/efs/GIT/PhotoPro/data/store/data_prepper_ALL-CATEGORIES.pkl')
    image_data, owner_data, pro_data = read_user_and_image_views(
                                                           all_images_prepper)
    # image_views.tolist()
    app.run(host='0.0.0.0', port=8080, threaded=True)
