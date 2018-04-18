from compute.modules import dataset
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Loads the dataset from csv file into pandas dataframe
df = dataset.loaddataframe('df.csv')

def maketraintestsplit(testsize):
    # Drop the feature called "Case" which I assume is whether or not the implant had to be removed - 0 for no, 1 for yes
    # Classifies the test cases into whether or not they have removed their implants
    X = df.drop('Case', axis=1)
    y = df['Case']

    # TODO implement gini index function instead of using sklearns split func?
    # these declarations make two pairs of sets
    # Xtrain and ytrain are training sets - X have all data except case, y contains only case
    # Xtest and ytest are test sets - X have all data except case, y contains only case
    # Test size is 30% (meaning training set is 70%), random_state is a pseudo-rng for random sampling
    x1, x2, y1, y2 = train_test_split(X, y, test_size=testsize)

    # TODO find better way to solve empty features
    # This replaces all empty fields with -1
    x1 = x1.fillna(-1)
    x2 = x2.fillna(-1)
    y1 = y1.fillna(-1)
    y2 = y2.fillna(-1)

    return x1, x2, y1, y2

def classify():
    xtrain, xtest, ytrain, ytest = maketraintestsplit(0.35)

    classifier = DecisionTreeClassifier()
    classifier.fit(xtrain, ytrain)

    ypred = classifier.predict(xtest)
    report = classification_report(ytest, ypred)

    print(confusion_matrix(ytest, ypred))
    print(report)
    return report
