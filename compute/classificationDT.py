import pandas as pd
import numpy as np

from sklearn import tree
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


dataframe = pd.read_csv('db.csv', sep=',')
print('Dataset length: ', len(dataframe))
print('Dataset shape: ', dataframe.shape)


print('dataframe::', dataframe.head())
dataframe.head()