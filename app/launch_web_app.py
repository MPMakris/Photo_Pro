#  -*- coding: utf-8 -*-
"""
Launch Script for Photo.Pro.

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
from scripts.get_info import (read_user_and_image_views, open_model,
                              get_overview_info)
import pandas as pd
import numpy as np
import pdb

#  Creat the Applicaiton:
app = Flask(__name__)


def turn_pred_to_list_of_list(pred, istart=1):
    """Format python data for the JS graphs."""
    output = []
    for i, value in enumerate(list(pred), start=istart):
        output.append([i, value])
    return output


def append_labels_to_UIP_data(pred):
    """Format python data for the JS pie chart."""
    output = []
    for label, value in zip(["Not Pro", "Pro"], list(pred)):
        output.append([["label", label], ["data", value]])
    return output


def try_getting_info():
    """Read the Directories."""
    # try:
    print "Building References..."
    (num_images, num_models, image_names, image_paths, model_names,
        model_paths) = get_overview_info()
    print "References Built."
    return (num_images, num_models, image_names, image_paths, model_names,
            model_paths)
    # except:
    #     print "Error Getting Basic Info from Directories."


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
    (num_images, num_models, image_names, image_paths, model_names,
        model_paths) = try_getting_info()
    return render_template('analytics/overview.html', num_images=num_images,
                           num_models=num_models, image_views=image_data,
                           user_total_views=owner_data, user_is_pro=pro_data)
#  user_is_pro=pro_data)


@app.route('/overview_with_data')
def overview_with_data():
    """Show the Overview page."""
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
    # pdb.set_trace()
    check = True
    while check:
        image_to_display_path = list(np.random.choice(image_paths, size=1,
                                                      replace=False,
                                                      p=None))[0]
        # pdb.set_trace()
        image_to_display_name = get_file_name_from_path(image_to_display_path)
        owner_name = image_to_display_name[:image_to_display_name.find('_')]
        image_id = image_to_display_name[image_to_display_name.find('_')+1:]
        image_id = image_id[:image_id.find('.')]
        #  Check that the image actually exists in the DataFrame:
        if ((int(image_id) not in X_combined.index.get_level_values(1)) or
                (owner_name not in X_combined.index.get_level_values(0))):
            check = True
            continue
        # Get Image Data:
        image_X = X_combined.loc[owner_name].loc[int(image_id)].reshape(
                                                                    (1, -1))
        image_y = y_combined.loc[owner_name].loc[int(image_id)].reshape(
                                                                    (1, -1))
        check = False
    # Get Prediced Probabilities:
    uip_proba = GBC_model_ANIMALS_uip.predict_proba(image_X).reshape((-1,))
    ivq_proba = GBC_model_ALL_CATEGORIES_ivq.predict_proba(
                                                        image_X).reshape((-1,))
    uvq_proba = GBC_model_ANIMALS_uvq.predict_proba(image_X).reshape((-1,))
    # Convert to JS style:
    uvq_proba = turn_pred_to_list_of_list(uvq_proba, 0)
    uip_proba_0 = uip_proba[0]
    uip_proba_1 = uip_proba[1]
    ivq_proba = turn_pred_to_list_of_list(ivq_proba, 1)
    uvq_proba = turn_pred_to_list_of_list(uvq_proba, 1)
    # See Numbers Being Fed:
    print "UIP Value 0: ", uip_proba_0
    print "UIP Value 1: ", uip_proba_1
    return render_template('analytics/previous_results.html',
                           image_name=image_to_display_name,
                           image_path=image_to_display_path,
                           owner_name=owner_name,
                           image_id=image_id,
                           image_X=image_X, image_y=image_y,
                           uip_proba_0=uip_proba_0, uip_proba_1=uip_proba_1,
                           ivq_proba=ivq_proba, uvq_proba=uvq_proba)


@app.route('/models')
def models():
    """Display the models page."""
    (num_images, num_models, image_names, image_paths, model_names,
        model_paths) = try_getting_info()
    return render_template('analytics/models.html')


if __name__ == "__main__":
    #  Get Info:
    (num_images, num_models, image_names, image_paths, model_names,
        model_paths) = try_getting_info()
    print "Unpickling Data Prepper"
    all_images_prepper = open_prepper('/home/ubuntu/efs/GIT/Photo_Pro/' +
                                      'data/store/data_prepper_ALL-' +
                                      'CATEGORIES.pkl')
    print "Data Prepper Unpickled."
    (image_data, owner_data, pro_data,
        X_combined, y_combined) = read_user_and_image_views(
                                                        all_images_prepper)
    print "Unpickling ANIMALS GBC MODELS..."
    GBC_model_ANIMALS_uip = open_model(
        ('/home/ubuntu/efs/GIT/Photo_Pro/data/store/' +
         'GBC_model_user_is_pro_ANIMALS.pkl'))
    GBC_model_ANIMALS_ivq = open_model(
        ('/home/ubuntu/efs/GIT/Photo_Pro/data/store/' +
         'GBC_model_image_views_quantized_ANIMALS.pkl'))
    GBC_model_ANIMALS_uvq = open_model(
        ('/home/ubuntu/efs/GIT/Photo_Pro/data/store/' +
         'GBC_model_user_total_views_quantized_ANIMALS.pkl'))
    print "ANIMALS Models Unpickled"
    print "Unpickling ALL-Categories GBC MODEL..."
    GBC_model_ALL_CATEGORIES_ivq = open_model(
        ('/home/ubuntu/efs/GIT/Photo_Pro/data/store/' +
         'classification_model_GBC_ALL-CATEGORIES_500.pkl'))
    print "ALL-CATEGORIES Model Unpickled"
    # <!-- Unpickling ALL MODELS -->
    # print "Unpickling BUIDLING MODELS..."
    # GBC_model_BUILDING_uip = open_model(
    #     ('/home/ubuntu/efs/GIT/Photo_Pro/data/store/' +
    #      'GBC_model_user_is_pro_BUILDING.pkl'))
    # GBC_model_BUILDING_ivq = open_model(
    #     ('/home/ubuntu/efs/GIT/Photo_Pro/data/store/' +
    #      'GBC_model_image_views_quantized_BUILDING.pkl'))
    # GBC_model_BUILDING_uvq = open_model(
    #     ('/home/ubuntu/efs/GIT/Photo_Pro/data/store/' +
    #      'GBC_model_user_total_views_quantized_BUILDING.pkl'))
    # print "Unpickling LANDSCAPE MODELS..."
    # GBC_model_LANDSCAPE_uip = open_model(
    #     ('/home/ubuntu/efs/GIT/Photo_Pro/data/store/' +
    #      'GBC_model_user_is_pro_LANDSCAPE.pkl'))
    # GBC_model_LANDSCAPE_ivq = open_model(
    #     ('/home/ubuntu/efs/GIT/Photo_Pro/data/store/' +
    #      'GBC_model_image_views_quantized_LANDSCAPE.pkl'))
    # GBC_model_LANDSCAPE_uvq = open_model(
    #     ('/home/ubuntu/efs/GIT/Photo_Pro/data/store/' +
    #      'GBC_model_user_total_views_quantized_LANDSCAPE.pkl'))
    # print "Unpickling PORTRAIT MODELS..."
    # GBC_model_PORTRAIT_uip = open_model(
    #     ('/home/ubuntu/efs/GIT/Photo_Pro/data/store/' +
    #      'GBC_model_user_is_pro_PORTRAIT.pkl'))
    # GBC_model_PORTRAIT_ivq = open_model(
    #     ('/home/ubuntu/efs/GIT/Photo_Pro/data/store/' +
    #      'GBC_model_image_views_quantized_PORTRAIT.pkl'))
    # GBC_model_PORTRAIT_uvq = open_model(
    #     ('/home/ubuntu/efs/GIT/Photo_Pro/data/store/' +
    #      'GBC_model_user_total_views_quantized_PORTRAIT.pkl'))
    # print "Unpickling SPORTS MODELS..."
    # GBC_model_SPORTS_uip = open_model(
    #     ('/home/ubuntu/efs/GIT/Photo_Pro/data/store/' +
    #      'GBC_model_user_is_pro_SPORTS.pkl'))
    # GBC_model_SPORTS_ivq = open_model(
    #     ('/home/ubuntu/efs/GIT/Photo_Pro/data/store/' +
    #      'GBC_model_image_views_quantized_SPORTS.pkl'))
    # GBC_model_SPORTS_uvq = open_model(
    #     ('/home/ubuntu/efs/GIT/Photo_Pro/data/store/' +
    #      'GBC_model_user_total_views_quantized_SPORTS.pkl'))
    # print "ALL Models Unpickled"
    # <-- /.Unpickling ALL MODELS -->
    app.run(host='0.0.0.0', port=8080, threaded=True)
