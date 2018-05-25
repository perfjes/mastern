
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def classify(df, testsize):
    x = df.drop('Case', axis=1)
    y = df['Case']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=testsize)

    classifier = DecisionTreeClassifier()
    classifier = classifier.fit(x_train, y_train)
    y_prediction = classifier.predict(x_test)
    return classification_report(y_test, y_prediction)

