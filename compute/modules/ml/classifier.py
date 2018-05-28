from compute.modules import graph_factory as g_factory, datahandler as dth
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


# Now stores the model after training, and for every run uses the stored model (if it exists)
# That should remove the runtime needed to retrain the model for each run
# But it introduces the problem of test-size variations - how to implement a check to retrain with new size?


def classify(df):
    x = df.drop('Case', axis=1)
    y = df['Case']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=dth.Data.split)

    classifier = dth.load_file('classifier.sav')
    if classifier is None:
        classifier = DecisionTreeClassifier()
        classifier = classifier.fit(x_train, y_train)
        dth.save_file('classifier.sav', classifier)

    y_prediction = classifier.predict(x_test)
    graph = g_factory.graph_factory(df)
    return classification_report(y_test, y_prediction), graph


def update_model(df):
    x = df.drop('Case', axis=1)
    y = df['Case']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=dth.Data.split)
    classifier = DecisionTreeClassifier()
    classifier = classifier.fit(x_train, y_train)
    dth.save_file('classifier.sav', classifier)
