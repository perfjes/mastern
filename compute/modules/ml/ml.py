from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import matplotlib as plt
import pandas as pd
from sklearn import metrics
from compute.modules import datahandler


dth = datahandler
discard_features_regression = ['volWear', 'volWearRate', 'Cr', 'Co', 'Zr', 'Ni', 'Mb']

def split_dataset_into_train_test(df, column, test_size):
    # Drop the feature called "Case" which I assume is whether or not the implant had to be removed, 0 for no, 1 for yes
    # Classifies the test cases into whether or not they have removed their implants
    x = df.drop(column, axis=1)
    y = df[column]

    # these declarations make two pairs of sets
    # Xtrain and ytrain are training sets - X have all data except case, y contains only case
    # Xtest and ytest are test sets - X have all data except case, y contains only case
    # Test size is 30% (meaning training set is 70%), random_state is a pseudo-rng for random sampling
    return train_test_split(x, y, test_size=test_size)


def regress(df):
    print(df.describe())
    xtrain, xtest, ytrain, ytest = split_dataset_into_train_test(df, 'years in vivo', dth.Data.split)
    regressor = DecisionTreeRegressor(max_depth=4)
    regressor.fit(xtrain, ytrain)
    ypred = regressor.predict(xtest)
    result = pd.DataFrame({'Actual': ytest, 'Predicted': ypred})
    meanlist = df['years in vivo'].tolist()
    mae = metrics.mean_absolute_error(ytest, ypred)
    #plottern = plt.scatter((df['Case']), df['years in vivo'])
    return result, mae


def target_regress(df, target):
    xtrain, xtest, ytrain, ytest = split_dataset_into_train_test(df, 'years in vivo', dth.Data.split)
    reg = DecisionTreeRegressor()
    reg.fit(xtrain, ytrain)
    targetpred = target.drop('years in vivo', axis=1)
    result = reg.predict(targetpred)
    ret = pd.DataFrame({'Actual': target['years in vivo'], 'Predicted': result})

    return ret


# Function for predicting the longevity of test set. Modify this to work on a singular entry (as with the target
# regress).
def predict_longevity(df):
    for feature in discard_features_regression:
        df = df.drop(feature, axis=1)
    x_train, x_test, y_train, y_test = split_dataset_into_train_test(df, 'years in vivo', dth.Data.split)
    if dth.load_file('regressor-model.sav') is None:
        regressor = DecisionTreeRegressor()
        regressor.fit(x_train, y_train)
        update_model(regressor)
    else:
        regressor = dth.load_file('regressor-model.sav')
    y_prediction = regressor.predict(x_test)
    result = pd.DataFrame({'Actual': y_test, 'Predicted': y_prediction})
    return result


def update_model(model):
    dth.save_file('regressor-model.sav', model)
