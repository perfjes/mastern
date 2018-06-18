from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn import metrics
from compute.modules import datahandler

# TODO better the module (no need to pass DF as parameter - call directly from datahandler
dth = datahandler
discard_features_regression = ['volWear', 'volWearRate', 'Cr', 'Co', 'Zr', 'Ni', 'Mb']


def split_dataset_into_train_test(df, column):
    x = df.drop(column, axis=1)
    y = df[column]
    return train_test_split(x, y, test_size=dth.Data.split)


def regress(df):
    x_train, x_test, y_train, y_test = split_dataset_into_train_test(df, 'years in vivo')
    if dth.load_pickle_file('regressor-model.sav') is None:
        regressor = DecisionTreeRegressor()
        regressor.fit(x_train, y_train)
        update_regression_model(regressor)
    else:
        regressor = dth.load_pickle_file('regressor-model.sav')
    y_pred = regressor.predict(y_test)
    result = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
    mae = metrics.mean_absolute_error(y_test, y_pred)
    return result, mae


# Function for predicting the longevity of test set. Modify this to work on a singular entry (as with the target
# regress).
def predict_longevity(df):
    df = prune_features(df)
    x_train, x_test, y_train, y_test = split_dataset_into_train_test(df, 'years in vivo')
    if dth.load_pickle_file('regressor-model.sav') is None:
        regressor = DecisionTreeRegressor()
        regressor.fit(x_train, y_train)
        update_regression_model(regressor)
    else:
        regressor = dth.load_pickle_file('regressor-model.sav')
    y_prediction = regressor.predict(x_test)
    result = pd.DataFrame({'Actual': y_test, 'Predicted': y_prediction})
    y_true = y_test.values.reshape(-1, 1)
    y_pred = y_prediction.reshape(-1, 1)
    r2 = metrics.r2_score(y_true, y_pred)
    return result, r2


# Function for predicting the longevity of a single sample - given the training/testing dataset and a new CSV file
# containing the exact same features as the training/testing set.
def target_predict_longevity(df, target):
    df = prune_features(df)
    target = prune_features(target)
    targetpred = target.drop('years in vivo', axis=1)
    x_train, x_test, y_train, y_test = split_dataset_into_train_test(df, 'years in vivo')
    if dth.load_pickle_file('regressor-model.sav') is None:
        regressor = DecisionTreeRegressor()
        regressor.fit(x_train, y_train)
        update_regression_model(regressor)
    else:
        regressor = dth.load_pickle_file('regressor-model.sav')
    y_prediction = regressor.predict(targetpred)
    result = pd.DataFrame({'Actual': target['years in vivo'], 'Predicted': y_prediction})
    return result, target


def update_regression_model(model):
    dth.save_file('regressor-model.sav', model)


# Removes all features from the pandas dataframe that are irrelevant (based on Petes suggestions)
# TODO figure out which values are important?
def prune_features(df):
    for feature in discard_features_regression:
        df = df.drop(feature, axis=1)
    return df
