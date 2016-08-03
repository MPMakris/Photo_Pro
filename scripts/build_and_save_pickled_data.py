"""A script to build all the final modeling datasets."""
import pandas as pd
from common.data_preparation import data_prepper
from common.os_interaction import get_file_name_from_path
import sys


def create_categorical_dataframes(feature_file, target_file):
    """Create train and test data based on ."""
    #  Status Messages:
    print "Starting Data Prep On:"
    print "-->\033[1;36m{}\033[0m".format(feature_file)
    print "-->\033[1;36m{}\033[0m".format(target_file)

    #  Get Search Term:
    file_name = get_file_name_from_path(feature_file)
    search_term = file_name[len('feature_data_'):]
    search_term = search_term[:search_term.find('_')]

    #  Load in Data:
    df_features = pd.read_csv(feature_file, sep='|', index_col=None)
    df_targets = pd.read_csv(target_file, sep='|', index_col=0)
    df_features = df_features.set_index('owner').set_index("id", append=True)
    df_targets = df_targets.set_index('owner').set_index("id", append=True)
    df_targets = df_targets.drop('image_tags', axis=1)

    #  Identify Target Columns:
    target_columns = list(df_targets.columns)
    target_columns.remove('image_ntags')

    #  Join DataFrams and Drop Bad Rows:
    df = df_features.join(df_targets, how='inner')
    df.dropna(axis=0, inplace=True)

    #  Begin Prepping:
    current_prepper = data_prepper(df, target_columns)
    current_prepper.fit_transform_quantile_col('image_views', 10)
    current_prepper.fit_transform_quantile_col('user_total_views', 10)
    current_prepper.fit_transform_binning_col('image_nfavs', [0., 10., 20.,
                                                              40., 80.,
                                                              150.,
                                                              300., 600.,
                                                              900., 1200.,
                                                              2000.])
    current_prepper.fit_transform_binning_col('image_ncomments', [0., 10.,
                                                                  20.,
                                                                  40., 80.,
                                                                  150., 300.,
                                                                  600., 900.,
                                                                  1200.,
                                                                  2000.])
    current_prepper.fit_transform_binning_col('image_nsets', [0., 5., 10.,
                                                              15., 20., 25.,
                                                              30., 35.])
    current_prepper.fit_transform_binning_col('image_npools', [0., 10., 20.,
                                                               40., 80.,
                                                               150., 300.,
                                                               600., 900.,
                                                               1200., 2000.])

    #  Status Message:
    print "Data Prep Complete for \033[1;36m{}\033[0m\n".format(search_term)
    return current_prepper, search_term


def create_all_categories_dataframe(feature_file_list, target_file_list):
    """Create train and test data based on ."""
    search_term = "ALL-CATEGORIES"
    #  Status Messages:
    print "Starting Data Prep On \033[1;36m{}\033[0m:".format(search_term)

    #  Read in Data:
    for i, (feature_file, target_file) in enumerate(zip(feature_file_list,
                                                        target_file_list)):
        if i == 0:
            df_features_all = pd.read_csv(feature_file, sep='|',
                                          index_col=None)
            df_targets_all = pd.read_csv(target_file, sep='|',
                                         index_col=0)
        else:
            df_features = pd.read_csv(feature_file, sep='|', index_col=None)
            df_targets = pd.read_csv(target_file, sep='|', index_col=0)
            df_features_all = pd.concat((df_features_all, df_features), axis=0)
            df_targets_all = pd.concat((df_targets_all, df_targets), axis=0)
            del df_features
            del df_targets

    #  Reindex To Same Indices:
    df_features_all = df_features_all.set_index('owner').set_index("id",
                                                                   append=True)
    df_targets_all = df_targets_all.set_index('owner').set_index("id",
                                                                 append=True)
    df_targets_all = df_targets_all.drop('image_tags', axis=1)

    #  Identify Target Columns:
    target_columns = list(df_targets_all.columns)
    target_columns.remove('image_ntags')

    #  Join DataFrams and Drop Bad Rows:
    df = df_features_all.join(df_targets_all, how='inner')
    df.dropna(axis=0, inplace=True)

    #  Begin Prepping:
    all_data_prepper = data_prepper(df, target_columns)
    all_data_prepper.fit_transform_quantile_col('image_views', 10)
    all_data_prepper.fit_transform_quantile_col('user_total_views', 10)
    all_data_prepper.fit_transform_binning_col('image_nfavs', [0., 10., 20.,
                                                               40., 80.,
                                                               150.,
                                                               300., 600.,
                                                               900., 1200.,
                                                               2000.])
    all_data_prepper.fit_transform_binning_col('image_ncomments', [0., 10.,
                                                                   20.,
                                                                   40., 80.,
                                                                   150., 300.,
                                                                   600., 900.,
                                                                   1200.,
                                                                   2000.])
    all_data_prepper.fit_transform_binning_col('image_nsets', [0., 5., 10.,
                                                               15., 20., 25.,
                                                               30., 35.])
    all_data_prepper.fit_transform_binning_col('image_npools', [0., 10., 20.,
                                                                40., 80.,
                                                                150., 300.,
                                                                600., 900.,
                                                                1200., 2000.])

    #  Status Message:
    print "Data Prep Complete for \033[1;36m{}\033[0m\n".format(search_term)
    return all_data_prepper, search_term


def save_prepper(prepper, destination_folder, search_term):
    """Save the :class:Data_Prepper object."""
    print "Saving \033[1;36m{}\033[0m Data Prepper...".format(search_term)
    file_name = "data_prepper_" + search_term
    prepper.save(destination_folder, file_name)
    print "Data Prepper Saved to:"
    print "-->\033[1;36m{}\033[0m\n".format(destination_folder + file_name +
                                            ".pkl")


def main(destination_folder):
    """Run the main sequence of functions."""
    feature_file_list = ['data/modeling/ANIMALS/feature_data_ANIMALS_36649.csv',
                         'data/modeling/BUILDING/feature_data_BUILDING_20293.csv',
                         'data/modeling/LANDSCAPE/feature_data_LANDSCAPE_44173.csv',
                         'data/modeling/PORTRAIT/feature_data_PORTRAIT_34669.csv',
                         'data/modeling/SPORTS/feature_data_SPORTS_21205.csv']
    target_file_list = ['data/modeling/ANIMALS/target_data_ANIMALS_36649.csv',
                        'data/modeling/BUILDING/target_data_BUILDING_20293.csv',
                        'data/modeling/LANDSCAPE/target_data_LANDSCAPE_44173.csv',
                        'data/modeling/PORTRAIT/target_data_PORTRAIT_34669.csv',
                        'data/modeling/SPORTS/target_data_SPORTS_21205.csv']

    #  Create and Save Preppers for Each Category:
    for feature_file, target_file in zip(feature_file_list, target_file_list):
        (current_prepper,
            search_term) = create_categorical_dataframes(feature_file,
                                                         target_file)
        save_prepper(current_prepper, destination_folder, search_term)

    #  Create and Save Prepper for ALL CATEGORIES COMBINED:
    # all_data_prepper, search_term = create_all_categories_dataframe(
    #                                       feature_file_list, target_file_list)
    # save_prepper(all_data_prepper, destination_folder, search_term)


if __name__ == "__main__":
    """
    Sys.Arg[0] : This File
    Sys.Arg[1] : Destination Folder Where Pickles to Be Saved
    """
    print ""
    destination_folder = str(sys.argv[1])
    if destination_folder[-1] != '/':
        destination_folder = destination_folder + '/'
    main(destination_folder)
