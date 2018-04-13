from compute.modules import dataset
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import tree


df = dataset.loaddataframe('df.csv')

print(list(df))

X = df.drop('Case', axis=1)
y = df['Case']

# TODO implement gini index function instead of using sklearn?

Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.30) #this can't be passed with NaN, but how solve?
classifier = DecisionTreeClassifier()
classifier.fit(Xtrain, ytrain)

ypred = classifier.predict(Xtest)
print(ypred)