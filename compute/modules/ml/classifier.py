from compute.modules import datahandler
from sklearn import tree
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix


def maketraintestsplit(df, testsize):
    # Drop the feature called "Case" which I assume is whether or not the implant had to be removed, 0 for no, 1 for yes
    # Classifies the test cases into whether or not they have removed their implants
    X = df.drop('Case', axis=1)
    y = df['Case']

    # TODO implement gini index function instead of using sklearns split func?
    # these declarations make two pairs of sets
    # Xtrain and ytrain are training sets - X have all data except case, y contains only case
    # Xtest and ytest are test sets - X have all data except case, y contains only case
    # Test size is 30% (meaning training set is 70%), random_state is a pseudo-rng for random sampling
    xtrain, xtest, ytrain, ytest = train_test_split(X, y, test_size=testsize)

    return xtrain, xtest, ytrain, ytest


def classify(df, testsize):
    xtrain, xtest, ytrain, ytest = maketraintestsplit(df, testsize)

    classifier = DecisionTreeClassifier()
    classifier = classifier.fit(xtrain, ytrain)

    ypred = classifier.predict(xtest)
    report = classification_report(ytest, ypred)

    # print(confusion_matrix(ytest, ypred))
    print(report)
    return report
