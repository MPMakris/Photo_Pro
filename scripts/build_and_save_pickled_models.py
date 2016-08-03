"""A script to build and save all the final models."""
from sklearn.ensemble import (RandomForestClassifier, RandomForestRegressor,
                              AdaBoostClassifier, GradientBoostingClassifier)
from sklearn.linear_model import (LogisticRegression, LinearRegression,
                                  LogisticRegressionCV, Lasso, Ridge,
                                  RidgeClassifier, SGDClassifier)
from sklearn.cross_validation import train_test_split
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             precision_recall_curve, f1_score, r2_score,
                             precision_recall_fscore_support)
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from scipy.stats import (randint as sp_randint, gamma as sp_gamma,
                         expon as sp_expon, uniform as sp_uniform)
from sklearn.grid_search import RandomizedSearchCV
import cPickle as pickle
import sys
import time
import os
from common.os_interaction import get_file_name_from_path

import pdb


def open_prepper(file_path):
    """Open the DataPrepper from pickled file."""
    with open(file_path) as f:
        prepper = pickle.load(f)
    return prepper


def save_model(directory, model_type_prefix, target_name, search_term, model):
    """Pickle the model."""
    print "Saving Model..."
    if directory[-1] != '/':
        directory = directory + '/'
    file_path_to_save = (directory +
                         "{}_model_{}_{}.pkl").format(model_type_prefix,
                                                      target_name,
                                                      search_term)
    with open(file_path_to_save, 'w') as f:
        pickle.dump(model, f)
    print "{}_{} Model Saved to:".format(model_type_prefix, target_name)
    print "-->\033[1;36m{}\033[0m\n".format(file_path_to_save)


def make_f1_and_acc_plot(model_name, best_model, X_test, y_test_col,
                         x_axis_name):
    """Create and save the best_model accuracy and F1 plot."""
    return


def get_random_grid_CV_params():
    """Define the Random Grid Search parameters for each model."""
    logit_params = {"C": sp_expon(loc=0.001, scale=1),
                    "fit_intercept": [True, False],
                    "intercept_scaling": sp_randint(1, 5),
                    "warm_start": [False, True]
                    }
    rf_params = {"min_samples_split": sp_randint(1, 50),
                 "min_samples_leaf": sp_randint(1, 50),
                 "criterion": ["gini", "entropy"],
                 "class_weight": ['balanced', 'balanced_subsample']
                 }
    ada_dt_params = {"learning_rate": sp_expon(loc=0.001, scale=1.5),
                     "algorithm": ['SAMME.R', 'SAMME']
                     }
    gbc_params = {"learning_rate": sp_expon(loc=0.001, scale=0.5),
                  "subsample": sp_uniform(loc=0.2, scale=0.8),
                  "max_features": [None, 'auto'],
                  "warm_start": [True, False],
                  "max_depth": [3, 4, 5],
                  }
    svc_params = {"C": sp_expon(loc=0.001, scale=2),
                  "kernel": ['rbf', 'poly'],
                  "degree": sp_randint(2, 10),
                  "coef0": [0, 1, 2],
                  "shrinking": [True, False]
                  }
    rnd_CV_param_distributions = {'Logistic': logit_params,
                                  'RandomForest': rf_params,
                                  'AdaBoost_DT': ada_dt_params,
                                  'GBC': gbc_params,
                                  'SVC': svc_params
                                  }
    return rnd_CV_param_distributions


def find_best_RF_model(search_term, target_name, X_train, X_test, y_train_col,
                       y_test_col, params, n_estimators=500, n_iters=10, cv=5):
    """Random search for best RF model, then eval. it and pickle the model."""
    print "\n-----BEGIN RANDOM FOREST CV-----"
    print "TARGET: \033[1;36m{}\033[0m".format(target_name)
    print "Searching for Best RF Model..."
    pdb.set_trace()
    y_train_col = y_train_col.astype(int)
    y_test_col = y_test_col.astype(int)
    model_RandomForest = RandomForestClassifier(n_jobs=36, random_state=42,
                                                verbose=0, oob_score=False,
                                                warm_start=False)
    CV_search_RandomForest = RandomizedSearchCV(estimator=model_RandomForest,
                                                param_distributions=params,
                                                n_iter=n_iters, n_jobs=1,
                                                cv=cv, verbose=0,
                                                random_state=30,
                                                error_score=0)
    CV_search_RandomForest.fit(X_train, y_train_col)
    print "RF Search \033[0;32mCOMPLETE\033[0m"
    best_RandomForest = CV_search_RandomForest.best_estimator_
    y_pred = best_RandomForest.predict(X_test).astype(int)
    #  pdb.set_trace()
    f1_best_RF = f1_score(y_test_col, y_pred, labels=None, pos_label=None,
                          average='weighted')
    precision_best_RF = precision_score(y_test_col, y_pred, pos_label=None,
                                        average='weighted')
    recall_best_RF = recall_score(y_test_col, y_pred, pos_label=None,
                                  average='weighted')
    acc_best_RF = accuracy_score(y_test_col, y_pred)
    print "Best Random Forest Classifier Scores (Weighted):"
    print ("| F1: {:0.3} | Precision: {:0.3} | Recall: {:0.3} |" +
           " Accuracy: {:0.3} |").format(f1_best_RF, precision_best_RF,
                                         recall_best_RF, acc_best_RF)
    #  FILL IN PRINTING ROUTINE HERE!
    print "\nF1 & Accuracy Plot Saved to:"
    print "-->\033[1;36m{}\033[0m".format("insert file_path here")
    print "--------------------------------\n"
    return best_RandomForest


def main(file_path):
    """Run the Main script to build the models."""
    directory = os.path.dirname(file_path)
    file_name = get_file_name_from_path(file_path)
    search_term = file_name[len("data_prepper_"):]
    search_term = search_term[:search_term.find(".pkl")]
    #  Unpickle the Dataset:
    print "\n----BEGIN MODELING FOR \033[1;36m{}\033[0m----".format(
                                                                  search_term)
    print "Unpickling \033[1;36m{}\033[0m...".format(file_name)
    prepper = open_prepper(file_path)
    #  Extract the Data:
    X_train, y_train = prepper.return_training_data()
    X_test, y_test = prepper.return_testing_data()
    print "{} Data Extraction \033[0;32mCOMPLETE\033[0m".format(search_term)
    #  Get Search Parameters:
    rnd_CV_param_distributions = get_random_grid_CV_params()

    target_columns_classifiers = ['user_is_pro',
                                  'image_views_quantized',
                                  'user_total_views_quantized',
                                  'image_nfavs_binned',
                                  'image_ncomments_binned',
                                  'image_nsets_binned',
                                  'image_npools_binned']

    for target_name in target_columns_classifiers:
        #  store =
        try:
            best_RF_model = find_best_RF_model(search_term, target_name,
                                               X_train, X_test,
                                               y_train[target_name],
                                               y_test[target_name],
                                               rnd_CV_param_distributions[
                                                              'RandomForest'],
                                               n_estimators=100, n_iters=5,
                                               cv=5)
            save_model(directory, "RF", target_name, search_term,
                       best_RF_model)
            print "\033[1;36m{}\033[0m Random Forest Complete at {}.".format(
                                      target_name, time.strftime("%Y-%m-%d %H:%M:%S"))
        except:
            print ("RF Model for Target \033[1;36m{}\033[0m" +
                   " \033[0;31mFAILED\033[0m").format(target_name)
            print "Proceeding to Next Model..."
            print "--------------------------------\n"

if __name__ == "__main__":
    """
    Sys.Arg[0] : This File
    Sys.Arg[1] : Pickled Data File
    """
    file_path = sys.argv[1]
    main(file_path)
