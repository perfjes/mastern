from compute.modules import dataSet

dataPath = r'../data/'

df = dataSet.createDataFrame(dataPath, 'db.csv')
dataSet.saveDataFrame(dataPath, df)

df2 = dataSet.loadDataFrame(dataPath, 'df.csv')
print(df2)