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
    current_prepper.fit_transform_binning_col('image_nfavs', [0, 5, 10, 20, 40,
                                                              80, 200, 400])
    current_prepper.fit_transform_binning_col('image_ncomments', [0, 5, 10, 20,
                                                                  40, 80, 200,
                                                                  400])
    current_prepper.fit_transform_binning_col('image_nsets', [0, 5, 10, 20])
    current_prepper.fit_transform_binning_col('image_npools', [0, 5, 10, 20])

    #  Status Message:
    print "Data Prep Complete for \033[1;36m{}\033[0m\n".format(search_term)
    return current_prepper, search_term


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
    feature_file = 'data/modeling/feature_data_ANIMALS_36649.csv'
    target_file = 'data/modeling/target_data_ANIMALS_36649.csv'
    current_prepper, search_term = create_categorical_dataframes(feature_file,
                                                                 target_file)
    save_prepper(current_prepper, destination_folder, search_term)

    feature_file = 'data/modeling/feature_data_BUILDING_20293.csv'
    target_file = 'data/modeling/target_data_BUILDING_20293.csv'
    current_prepper, search_term = create_categorical_dataframes(feature_file,
                                                                 target_file)
    save_prepper(current_prepper, destination_folder, search_term)

    feature_file = 'data/modeling/feature_data_LANDSCAPE_44173.csv'
    target_file = 'data/modeling/target_data_LANDSCAPE_44173.csv'
    current_prepper, search_term = create_categorical_dataframes(feature_file,
                                                                 target_file)
    save_prepper(current_prepper, destination_folder, search_term)

    feature_file = 'data/modeling/feature_data_PORTRAIT_34669.csv'
    target_file = 'data/modeling/target_data_PORTRAIT_34669.csv'
    current_prepper, search_term = create_categorical_dataframes(feature_file,
                                                                 target_file)
    save_prepper(current_prepper, destination_folder, search_term)

    feature_file = 'data/modeling/feature_data_SPORTS_21205.csv'
    target_file = 'data/modeling/target_data_SPORTS_21205.csv'
    current_prepper, search_term = create_categorical_dataframes(feature_file,
                                                                 target_file)
    save_prepper(current_prepper, destination_folder, search_term)

if __name__ == "__main__":
    """
    Sys.Arg[0] : This File
    Sys.Arg[1] : Destination Folder
    """
    destination_folder = str(sys.argv[1])
    if destination_folder[-1] != '/':
        destination_folder = destination_folder + '/'
    main(destination_folder)
