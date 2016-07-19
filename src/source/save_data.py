"""Methods for saving API data to DataFrames and CSV files."""
import pandas as pd


def create_dataframe_from_soup_objects(picture_soup_data):
    columns = picture_soup_data[0].attrs.keys()
    data_content = []
    num_soups = len(picture_soup_data)
    for i, mini_soup in enumerate(picture_soup_data):
        data_content.append([int(mini_soup.get(name)) for name in columns])
        if i % (num_soups/10) == 0:
            print "   ...{:.0f} Percent Complete".format(float(i)/len(picture_soup_data)*100)
    df = pd.DataFrame(data=picture_data, columns=columns)
    print "DataFrame COMPLETE"
    return df

def save_dataframe(df, filename):
    df.to_csv(filename, header=True, index=True, index_label=False, mode='wb')
    print "Data Saved to {}".format(filename.upper())
