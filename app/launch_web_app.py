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

@app.route('/analytics')
def analytics_page():
    """Display the analytics page."""
    return render_template('analytics/charts.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
