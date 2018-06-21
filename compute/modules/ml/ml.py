from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn import metrics
from compute.modules import datahandler

# TODO minmaxscaler (morten)
dth = datahandler
features_regression = ['case', 'volwear', 'volwearrate', 'cr', 'co', 'zr', 'ni', 'mb']
sexes = ['male', 'female']


# Saving of split value in mutatable variable makes it possible to detect changes to split value and retrain the
# models should a change be present.
class Data:
    split = dth.Data.split


# Takes two parameters; dataframe contains the dataset to be split into testing and training datasets, and column is
# the variable that determines the split
def split_dataset_into_train_test(dataframe, column):
    x = dataframe.drop(column, axis=1)
    y = dataframe[column]
    return train_test_split(x, y, test_size=dth.Data.split, random_state=55)


# Tests the regression model on the currently loaded dataset, prints the predicted results and the actual results for
# simple comparison, prints the mean absoulte error to the console
def regress():
    df = dth.Data.dataframe
    x_train, x_test, y_train, y_test = split_dataset_into_train_test(df, 'years in vivo')

    # Checks if whether a regressor model is saved and the split value hasn't changed
    if dth.load_pickle_file('regressor-model.sav') is not None and Data.split == dth.Data.split:
        regressor = dth.load_pickle_file('regressor-model.sav')
    else:
        regressor = update_regression_model(df)

    y_pred = regressor.predict(y_test)
    result = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
    mae = metrics.mean_absolute_error(y_test, y_pred)
    print(mae)
    return result, mae


# Function for predicting the longevity of test set. Modify this to work on a singular entry (as with the target
# regress).
def predict_longevity():
    df = prune_features(dth.Data.dataframe)
    x_train, x_test, y_train, y_test = split_dataset_into_train_test(df, 'years in vivo')

    # Checks if whether a regressor model is saved and the split value hasn't changed
    if dth.load_pickle_file('regressor-model.sav') is not None and Data.split == dth.Data.split:
        regressor = dth.load_pickle_file('regressor-model.sav')
    else:
        regressor = update_regression_model(df)

    try:
        y_prediction = regressor.predict(x_test)
    except ValueError:
        print('oops')

    result = pd.DataFrame({'Actual': y_test, 'Predicted': y_prediction})

    # Reshape the arrays to work with R2 score validator
    y_true = y_test.values.reshape(-1, 1)
    y_pred = y_prediction.reshape(-1, 1)
    r2 = metrics.r2_score(y_true, y_pred)
    return result, r2


# Function for predicting the longevity of a single sample - given the training/testing dataset and a new CSV file
# containing the exact same features as the training/testing set.
def target_predict_longevity(target):
    df = prune_features(dth.Data.dataframe)
    target = prune_features(target)
    targetpred = target.drop('years in vivo', axis=1)

    # Checks if whether a regressor model is saved and the split value hasn't changed
    if dth.load_pickle_file('regressor-model.sav') is not None and Data.split == dth.Data.split:
        regressor = dth.load_pickle_file('regressor-model.sav')
    else:
        regressor = update_regression_model(df)

    y_prediction = regressor.predict(targetpred)
    result = pd.DataFrame({'Actual': target['years in vivo'], 'Predicted': y_prediction})

    return result


def update_regression_model(df):
    Data.split = dth.Data.split
    x_train, x_test, y_train, y_test = split_dataset_into_train_test(df, 'years in vivo')
    regressor = DecisionTreeRegressor()
    regressor.fit(x_train, y_train)
    dth.save_file('regressor-model.sav', regressor)
    print('Saved new regression model')
    return regressor


# Removes all features from the pandas dataframe that are irrelevant (based on Petes suggestions)
# TODO figure out which values are important?
def prune_features(df):
    for feature in features_regression:
        df = df.drop(feature, axis=1)
    return df
