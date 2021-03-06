"""Methods for saving API data to DataFrames and CSV files."""
import pandas as pd
import sys


def create_dataframe_from_soup_objects(picture_soup_data):
    """Turn list of soup objects into a list of lists containing the data."""
    columns = set()
    for mini_soup in picture_soup_data:
        columns.update(mini_soup.attrs.keys())
    columns = list(columns)
    data_content = []
    num_soups = len(picture_soup_data)
    for i, mini_soup in enumerate(picture_soup_data):
        data_content.append(
                    [mini_soup.get(name, default="NaN") for name in columns])
        if i % (num_soups/10) == 0:
            sys.stdout.write("   ...{:.0f} Percent Complete\r".format(
                                        float(i)/len(picture_soup_data)*100))
            sys.stdout.flush()
    df = pd.DataFrame(data=data_content, columns=columns)
    print "DataFrame \033[0;32mCOMPLETE\033[0m                     "
    return df


def save_dataframe(df, filename):
    """Save DataFame to CSV."""
    df.to_csv(filename, header=True, index=True, index_label=False, mode='wb',
              encoding='utf-8', na_rep='NaN', sep='|')
    print "DataFrame Saved to:\n-->\033[1;36m{}\033[0m\n".format(filename)
