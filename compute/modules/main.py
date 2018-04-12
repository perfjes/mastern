from compute.modules import dataSet
from sklearn.tree import DecisionTreeClassifier, export_graphviz

dataPath = r'../data/'

df = dataSet.createDataFrame(dataPath, 'db.csv')

print("* Person ID", '\n', df["id"].unique())

dataSet.saveDataFrame(dataPath, df)

df2 = dataSet.loadDataFrame(dataPath, 'df.csv')
#print(df2)