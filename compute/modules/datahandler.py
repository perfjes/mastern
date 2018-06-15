from os.path import dirname, abspath
import pandas as pd
import os
import _pickle as pickle

# TODO add comparison between load and previously saved, in order to reduce redundancy on larger sets
from flask_restful import Resource

ROOT_DIRECTORY = dirname(dirname(abspath(__file__)))


class Path:
    path = '%s%s' % (ROOT_DIRECTORY, r'/data/')
    pickle_data = '%s%s' % (ROOT_DIRECTORY, r'/data/data.pkl')
    pickle_split = '%s%s' % (ROOT_DIRECTORY, r'/data/split.pkl')


# ---------- OBJECT SAVING AND LOADING ----------
# TODO - implement error handling on save/load, make sure values are correct etc
# Autosaves the dataframe to pickle
def autosave_dataframe_to_pickle(objects):
    with open(Path.pickle_data, 'wb') as output_data:
        pickle.dump(objects, output_data)


# Autosaves the split value to pickle
def autosave_split_to_pickle(objects):
    with open(Path.pickle_split, 'wb') as output_data:
        pickle.dump(objects, output_data)


# Loads the autosaved dataframe from cPickle
def load_dataframe_from_pickle():
    if os.path.isfile(Path.pickle_data):
        try:
            with open(Path.pickle_data, 'rb') as input_data:
                return pickle.load(input_data)
        except:
            data = pd.DataFrame()
            autosave_dataframe_to_pickle(data)
            return data
    else:
        data = pd.DataFrame()
        autosave_dataframe_to_pickle(data)
        return data


# Loads the split value from cPickle
def load_split_value_from_pickle():
    if os.path.isfile(Path.pickle_split):
        try:
            with open(Path.pickle_split, 'rb') as input_data:
                return pickle.load(input_data)
        except:
            split = 0.35
            autosave_split_to_pickle(split)
            return split
    else:
        split = 0.35
        autosave_split_to_pickle(split)
        return split


# Class variables allow for mutation
class Data(Resource):
    dataframe = load_dataframe_from_pickle()
    split = load_split_value_from_pickle()


# In case the system should be able to mutate the data, then it should be able to not overwrite the existing
# datasets.
def save_as_new(data):
    counter = 1
    save = 'df.csv'
    data_directory = dirname(Path.path) + '/'

    if not os.path.isfile(data_directory + save):
        data.to_csv(os.path.join(data_directory + save), encoding='utf-8', index=False)
        return save
    if os.path.isfile(data_directory + save):
        save = 'df' + str(counter) + '.csv'
        while os.path.isfile(data_directory + save):
            counter += 1
            save = 'df' + str(counter) + '.csv'
    if not os.path.isfile(data_directory + save):
        data.to_csv(os.path.join(data_directory + save), encoding='utf-8', index=False)
        print(os.path.join(data_directory + save))
        return save
    else:
        return 'Saving as new file did not work'


# Loads file from path, reads it as CSV and returns the result as a pandas dataframe (or series).
# This will also automatically fill all missing data with the mean value of each column.
# TODO implement optional filling of missing data (remove rows where data is missing)
# TODO cont. this has been avoided due to tiny dataset with no affordance to remove rows available.
# TODO cont. Implement error handling on file not found / wrong file type
# TODO - This has become quite messy, but the error handling has improved significantly. Maybe clean it up later.
def load_dataframe(path):
    default = 'db.csv'
    if not path == Path.path:
        if len(path.split('/')) <= 1:
            if path.endswith('.csv'):
                file = "%s%s" % (Path.path, path)
            elif path.endswith('/'):
                file = '%s%s' % (Path.path, default)
            else:
                file = "%s%s%s" % (Path.path, path, '.csv')
        else:
            file = path
    else:
        file = '%s%s' % (path, default)
    if not os.path.isfile(file):
        for root, dirs, files in os.walk(path):
            if file in files:
                data = pd.read_csv(file, sep=',')
                if data.isnull().values.any():
                    filled = data.fillna(data.mean(skipna=True))
                    return filled
                else:
                    return data

    data = pd.read_csv(file, sep=',', encoding='utf-8')

    if data.isnull().values.any():
        filled = data.fillna(data.mean(skipna=True))
        return filled
    else:
        return data


def filter_criterion(df, column, value):
    return df.loc[df[column] == value]


def update_pickle(data, split):
    Data.dataframe = data
    Data.split = split
    autosave_dataframe_to_pickle(data)
    autosave_split_to_pickle(split)


def save_file(file, item):
    file = '%s%s' % (Path.path, file)
    with open(file, 'wb') as output_data:
        pickle.dump(item, output_data)


def load_pickle_file(file):
    file = '%s%s' % (Path.path, file)
    if os.path.isfile(file):
        with open(file, 'rb') as input_data:
            return pickle.load(input_data)
    else:
        print('no')
        return None
