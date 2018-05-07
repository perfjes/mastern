from os.path import dirname
import pandas as pd
import os

# TODO add comparison between load and previously saved, in order to reduce redundancy on larger sets

# TODO maybe make this a datahandler class - incorporate functions for splitting dataset based on user input /
# prediction criteria?

path = '%s%s' % (dirname(os.getcwd()), r'/data/')


class Dataset:
    # filename = 'df.csv'
    dataframe = pd.DataFrame()


# Overwrite default df.csv file.
def savedataframe(data):
    data.to_csv(os.path.join(path, r'df.csv'), encoding='utf-8', index=False)


# In case the system should be able to mutate the data, then it should be able to not overwrite the existing
# datasets.
def saveasnew(data):
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
def loaddataframe(filename):
    if filename.endswith('.csv'):
        file = "%s%s" % (path, filename)
    else:
        file = "%s%s%s" % (path, filename, '.csv')
    data = pd.read_csv(file, sep=',')

    if data.isnull().values.any():
        filled = data.fillna(data.mean(skipna=True))
        Dataset.dataframe = filled
        return filled
    else:
        Dataset.dataframe = data
        return data


def filtercriterion(column, value):
    filtered = Dataset.dataframe.loc[Dataset.dataframe[column] == value]
    return filtered


