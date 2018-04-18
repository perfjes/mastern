from os.path import dirname, abspath
from pathlib import Path
import pandas as pd
import os

# TODO add comparison between load and previously saved, in order to reduce redundancy on larger sets

pathe = dirname(__file__)
path = os.path.join(pathe, '/')


def createdataframe(filename):
    file = "%s%s" % (path, filename)
    dataframe = pd.read_csv(file, sep=',')
    return dataframe


def savedataframe(data):
    data.to_csv(os.path.join(path, r'df.csv'), encoding='utf-8', index=False)


def saveasnew(data):
    counter = 0
    save = 'df.csv'
    while os.path.isfile(path + save):
        counter += 1
        if counter > 0:
            save = 'df' + str(counter) + '.csv'
            print('Dataframe saved as new file, named: ', save)
    data.to_csv(os.path.join(path, save))


def loaddataframe(filename):
    file = "%s%s" % (path, filename)
    dataframe = pd.read_csv(file, sep=',')
    return dataframe
