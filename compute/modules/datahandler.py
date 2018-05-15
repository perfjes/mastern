from os.path import dirname
import pandas as pd
import os
import _pickle as pickle

# TODO add comparison between load and previously saved, in order to reduce redundancy on larger sets

path = '%s%s' % (dirname(dirname(os.getcwd())), r'/data/')
pickle_data = '%s%s' % (path, r'data.pkl')
pickle_split = '%s%s' % (path, r'split.pkl')


# ---------- OBJECT SAVING AND LOADING ----------
# TODO - implement error handling on save/load, make sure values are correct etc
# Autosaves the dataframe to pickle
def autosave_dataframe_to_pickle(objects):
    with open(pickle_data, 'wb') as output_data:
        pickle.dump(objects, output_data)


# Autosaves the split value to pickle
def autosave_split_to_pickle(objects):
    with open(pickle_data, 'wb') as output_data:
        pickle.dump(objects, output_data)


# Loads the autosaved dataframe from cPickle
def load_dataframe_from_pickle():
    try:
        with open(pickle_data, 'rb') as input_data:
            return pickle.load(input_data)
    except:
        data = load_dataframe('df')
        autosave_dataframe_to_pickle(data)
        return data


# Loads the split value from cPickle
def load_split_value_from_pickle():
    try:
        with open(pickle_split, 'rb') as input_data:
            return pickle.load(input_data)
    except:
        split = 0.35
        autosave_split_to_pickle(split)
        return split


class Data:
    dataframe = load_dataframe_from_pickle()
    split = load_split_value_from_pickle()


# Overwrite default df.csv file.
def save_data_frame(data):
    data.to_csv(os.path.join(path, r'df.csv'), encoding='utf-8', index=False)


# In case the system should be able to mutate the data, then it should be able to not overwrite the existing
# datasets.
def save_as_new(data):
    counter = 0
    save = 'df.csv'
    while os.path.isfile(path + save):
        counter += 1
        if counter > 0:
            save = 'df' + str(counter) + '.csv'
            print('Dataframe saved as new file, named: ', save)
    data.to_csv(os.path.join(path, save))
    return save


# Loads file from path, reads it as CSV and returns the result as a pandas dataframe (or series).
# This will also automatically fill all missing data with the mean value of each column.
# TODO implement optional filling of missing data (remove rows where data is missing)
# TODO cont. this has been avoided due to tiny dataset with no affordance to remove rows available.
# TODO cont. Implement error handling on file not found / wrong file type
def load_dataframe(filename):
    if filename.endswith('.csv'):
        file = "%s%s" % (path, filename)
    else:
        file = "%s%s%s" % (path, filename, '.csv')
    data = pd.read_csv(file, sep=',')

    if data.isnull().values.any():
        filled = data.fillna(data.mean(skipna=True))
        return filled
    else:
        return data


def filter_criterion(df, column, value):
    return df.loc[df[column] == value]
