from os.path import dirname
from sklearn.preprocessing import Imputer
import pandas as pd
import os

# TODO add comparison between load and previously saved, in order to reduce redundancy on larger sets


directory = dirname(os.getcwd())
datapath = "/data/"
path = directory + datapath


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
def loaddataframe(filename):
    file = "%s%s" % (path, filename)
    data = pd.read_csv(file, sep=',')
    if(data.isnull().values.any()):
        filled = data.fillna(data.mean(skipna=True))
        return filled
    else:
        return data
