from compute.modules import dataset
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn import tree


# Loads the dataset from csv file into pandas dataframe
df = dataset.loaddataframe('df.csv')

# Drop the feature called "Case" which I assume is whether or not the implant had to be removed - 0 for no, 1 for yes
X = df.drop('Case', axis=1)
y = df['Case']

# TODO implement gini index function instead of using sklearns split func?
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.30)

# TODO find better way to solve empty features
Xtrain = Xtrain.fillna(-1)
Xtest = Xtest.fillna(-1)
ytrain = ytrain.fillna(-1)
ytest = ytest.fillna(-1)

classifier = DecisionTreeClassifier()
classifier.fit(Xtrain, ytrain)

ypred = classifier.predict(Xtest)

print(confusion_matrix(ytest, ypred))
print(classification_report(ytest, ypred))
