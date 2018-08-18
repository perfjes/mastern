from os.path import dirname, abspath
import pandas as pd
import os
import _pickle as pickle

ROOT_DIRECTORY = dirname(dirname(dirname(abspath(__file__))))


class Path:
    path = '%s%s' % (ROOT_DIRECTORY, r'/data/')
    result_json = '%s/data/test-results/' % ROOT_DIRECTORY
    pickle_data = '%s%s' % (ROOT_DIRECTORY, r'/data/data.pkl')
    pickle_split = '%s%s' % (ROOT_DIRECTORY, r'/data/split.pkl')


class Features:
    drop_features_regression = ['id', 'volwear', 'volwearrate']
    """
        List of all features in the dataset
        'id', 'case', 'cuploose', 'stemloose', 'years in vivo', 'cr', 'co', 'zr', 'ni', 'mb', 'linwear', 'linwearrate', 
        'volwear', 'volwearrate', 'inc', 'ant', 'cupx', 'cupy', 'male', 'female'
    """
    initially_deactivated = ['zr', 'ni', 'mb', 'cupx', 'cupy']


class Test_data:
    result_dt = {}


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


# Saves the results from GridSearchCV hyperparameter tuning as JSON.
def save_results(filename, data):
    counter = 1

    file_save = Path.result_json + filename + '.json'

    if os.path.isfile(file_save):
        file_save = Path.result_json + filename + str(counter) + '.json'
        while os.path.isfile(file_save):
            counter += 1
            file_save = Path.result_json + filename + str(counter) + '.json'

    if not os.path.isfile(file_save):
        with open(file_save, 'wb') as output_data:
            pickle.dump(data, output_data)
        return True, file_save
    else:
        return False


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

    # Turn the CSV file into a Pandas dataframe, then turn all columns into lowercase. Refactor columns where binary
    # values have a higher level of semantic value than 'yes/no', rename the results of these refactorings and
    # replace the original columns with the refactored ones.
    data = pd.read_csv(file, sep=',', encoding='utf-8')
    data = data.rename(str.lower, axis='columns')

    if 'sex' in data:
        refactored_columns = pd.get_dummies(data['sex'])
        refactored_columns = refactored_columns.rename(columns={1.0: 'male', 2.0: 'female'})
        data = data.drop('sex', axis=1)
        data = pd.concat([data, refactored_columns], axis=1)

    if 'id' in data:
        data = data.drop('id', axis=1)

    data = prune_features(data)

    # Fill in the blanks (with mean values for the mean time)
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


def load_file(file):
    file = '%s%s' % (Path.path, file)
    if os.path.isfile(file):
        with open(file, 'rb') as input_data:
            return pickle.load(input_data)
    else:
        print('The file couldn\'t be loaded')
        return None


def create_csv_from_html_input(input_list):
    # TODO create function to do this thing
    pass


def prune_features(df):
    for feature in Features.drop_features_regression:
        if feature in df:
            df = df.drop(feature, axis=1)
    return df


# Class variables allow for mutation
class Data:
    dataframe = load_dataframe_from_pickle()
    split = load_split_value_from_pickle()
    target = pd.DataFrame()
