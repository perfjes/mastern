from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeRegressor
from compute.modules import dataset
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn import metrics


def maketraintestsplit(df, column, testsize):
    # Drop the feature called "Case" which I assume is whether or not the implant had to be removed, 0 for no, 1 for yes
    # Classifies the test cases into whether or not they have removed their implants
    # TODO implement auto detect of which column to drop?
    X = df.drop(column, axis=1)
    y = df[column]

    # these declarations make two pairs of sets
    # Xtrain and ytrain are training sets - X have all data except case, y contains only case
    # Xtest and ytest are test sets - X have all data except case, y contains only case
    # Test size is 30% (meaning training set is 70%), random_state is a pseudo-rng for random sampling
    # TODO implement gini index function instead of using sklearns split func?

    return train_test_split(X, y, test_size=testsize)


def regress(file):
    df = dataset.loaddataframe(file)
    xtrain, xtest, ytrain, ytest = maketraintestsplit(df, 'years in vivo', 0.25)
    regressor = DecisionTreeRegressor(max_depth=1)

    print(xtrain.shape)
    regressor.fit(xtrain, ytrain)
    ypred = regressor.predict(xtest)
    result = pd.DataFrame({'Actual':ytest, 'Predicted':ypred})

    print(result, '\n')
    meanlist = df['years in vivo'].tolist()
    print(sum(meanlist) / float(len(meanlist)), '\n')
    mae = metrics.mean_absolute_error(ytest, ypred)
    print('Mean Absolute Error:', mae)
    r2 = r2_score(ytest, ypred)
    return mae, r2
