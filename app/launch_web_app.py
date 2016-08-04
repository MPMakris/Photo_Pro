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
#  Creat the Applicaiton:
app = Flask(__name__)


#  Main Landing Page:
@app.route('/')
@app.route('/index')
def landing_page():
    """Display the landing page."""
    return render_template('index.html')


@app.route('/analytics/overview')
def overview_page():
    """Display the overview page."""
    return render_template('analytics/overview.html')


@app.route('/analytics/analyze_photo/')
def upload_page():
    """Display the image upload page."""
    return render_template('analytics/analyze_photo.html')


@app.route('/analytics/analyze_photo/results')
def results_page(image):
    """Display the results page."""
    return render_template('results page')


@app.route('/analytics/previous_results')
def previous_results_page():
    """Display the previous results page."""
    return render_template('previous results page')


@app.route('/graph')
def image_page():
    """Display the graph."""
    return render_template('../../notebooks/lines.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
