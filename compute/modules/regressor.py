from sklearn.tree import DecisionTreeRegressor
from compute.modules import dataset
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn import metrics


df = dataset.loaddataframe('df.csv')

# AND NOW FOR SOME REGRESSION

def maketraintestsplit(column, testsize):


    # Drop the feature called "Case" which I assume is whether or not the implant had to be removed - 0 for no, 1 for yes
    # Classifies the test cases into whether or not they have removed their implants
    X = df.drop(column, axis=1)
    y = df[column]

    # TODO implement gini index function instead of using sklearns split func?
    # these declarations make two pairs of sets
    # Xtrain and ytrain are training sets - X have all data except case, y contains only case
    # Xtest and ytest are test sets - X have all data except case, y contains only case
    # Test size is 30% (meaning training set is 70%), random_state is a pseudo-rng for random sampling
    x1, x2, y1, y2 = train_test_split(X, y, test_size=testsize)

    # TODO find better way to solve empty features
    # This replaces all empty fields with -1
    x1 = x1.fillna(0)
    x2 = x2.fillna(0)
    y1 = y1.fillna(0)
    y2 = y2.fillna(0)

    return x1, x2, y1, y2

def regress():
    xtrain, xtest, ytrain, ytest = maketraintestsplit('years in vivo', 0.25)
    regressor = DecisionTreeRegressor()

    print(xtrain.shape)
    regressor.fit(xtrain, ytrain)
    ypred = regressor.predict(xtest)
    result = pd.DataFrame({'Actual':ytest, 'Predicted':ypred})

    print(result, '\n')
    meanlist = df['years in vivo'].tolist()
    print(sum(meanlist) / float(len(meanlist)), '\n')
    print('Mean Absolute Error:', metrics.mean_absolute_error(ytest, ypred))
