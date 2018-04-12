import pandas as pd

# TODO add comparison between load and previously saved, in order to reduce redundancy on larger sets

def createDataFrame(path, filename):
    file = "%s%s" % (path, filename)
    dataframe = pd.read_csv(file, sep = ',')
    return dataframe

def saveDataFrame(path, data):
    import os
    data.to_csv(os.path.join(path, r'df.csv'), encoding = 'utf-8', index = False)

def loadDataFrame(path, filename):
    file = "%s%s" % (path, filename)
    dataframe = pd.read_csv(file, sep = ',')
    return dataframe