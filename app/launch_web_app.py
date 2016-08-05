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
from scripts.common.os_interaction import get_file_name_from_path
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
    return render_template('analytics/overview.html', num_images=num_images,
                           num_models=num_models)


@app.route('/overview_with_data')
def overview_with_data():
    """Show the Overview page."""
    try:
        print "Unpickling Data Prepper"
        all_images_prepper = open_prepper(
                         '/home/ubuntu/efs/GIT/Photo_Pro/data/store/data_prepper_ALL-CATEGORIES.pkl')
    except:
        print "Error Unpickling Data Prepper..."
    image_data, owner_data, pro_data = read_user_and_image_views(
                                                           all_images_prepper)
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
    pdb.set_trace()
    images_to_display_paths = list(np.random.choice(image_paths, size=4,
                                                    replace=False, p=None))
    pdb.set_trace()
    images_to_display_names = []
    for image_path in images_to_display_paths:
        images_to_display_names.append(get_file_name_from_path(image_path))
    image_path_1 = images_to_display_paths[0]
    image_name_1 = images_to_display_names[0]
    return render_template('analytics/previous_results.html',
                           image_name_1=image_name_1,
                           image_path_1=image_path_1)


@app.route('/models')
def models():
    """Display the models page."""
    return render_template('analytics/models.html')


if __name__ == "__main__":
    try:
        print "Building References..."
        (num_images, num_models, image_names, image_paths, model_names,
            model_paths) = get_overview_info()
        print "References Built"
    except:
        print "Error Getting Basic Info from Directories"
    pdb.set_trace()
    #  image_views.tolist()
    app.run(host='0.0.0.0', port=8080, threaded=True)
