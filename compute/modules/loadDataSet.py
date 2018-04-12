import pandas as pd

# TODO add functionality that reads the file, compares to a db file saved from previous runs, fetches changes, saves new entries

def createDataFrame():
    dataframe = pd.read_csv('..\data\db.csv', sep=',')
    return dataframe
