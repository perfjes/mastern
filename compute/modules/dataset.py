import pandas as pd
import os

# TODO add comparison between load and previously saved, in order to reduce redundancy on larger sets

path = r'../data/'


def createdataframe(filename):
    file = "%s%s" % (path, filename)
    dataframe = pd.read_csv(file, sep=',')
    return dataframe


def savedataframe(data):
    data.to_csv(os.path.join(path, r'df.csv'), encoding='utf-8', index=False)


def loaddataframe(filename):
    file = "%s%s" % (path, filename)
    dataframe = pd.read_csv(file, sep=',')
    return dataframe
