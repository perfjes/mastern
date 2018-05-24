from tkinter import Image

import graphviz

from sklearn import tree
from sklearn.externals.six import StringIO
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pydotplus


def split_dataset_into_train_test(df, testsize):
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
    xtrain, xtest, ytrain, ytest = split_dataset_into_train_test(df, testsize)

    classifier = DecisionTreeClassifier()
    classifier = classifier.fit(xtrain, ytrain)

    ypred = classifier.predict(xtest)
    report = classification_report(ytest, ypred)

    dot_data = StringIO()
    export_graphviz(classifier, out_file=dot_data,
                    filled=True, rounded=True,
                    special_characters=True)

    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    print(report)
    return report, graph


# None of this works at all like I had planned
# TODO figure it out haha
# TODO also jesus christ I gotta step up the naming game
def target_classify(df, target, split):
    xtrain, xtest, ytrain, ytest = split_dataset_into_train_test(df, split)

    clas = DecisionTreeClassifier()
    clas = clas.fit(xtrain, ytrain)

    yes = target.drop('Case', axis=1)

    pls = clas.predict(yes)
    pls2 = clas.predict(xtest)

    report1 = classification_report(target['Case'], pls)
    report2 = classification_report(ytest, pls2)

    return report1, report2
