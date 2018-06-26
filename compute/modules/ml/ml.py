import csv

from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn import metrics
from compute.modules import datahandler, graph_factory

# TODO fiddle with decisiontreeregressor parameters to get better score
# TODO minmaxscaler (morten)
dth = datahandler
graph = graph_factory
features_regression = ['id', 'volwear', 'volwearrate', 'cr', 'co', 'zr', 'ni', 'mb']  # These are removed
sexes = ['male', 'female']  # These are added


# TODO få inn en lengde-sjekker på features? Evt om den har samme features? Åååhhh stress

# Saving of split value in mutatable variable makes it possible to detect changes to split value and retrain the
# models should a change be present.
class Data:
    split = dth.Data.split
    arthroplasty_dataset = list(dth.load_dataframe('db.csv'))  # the original file TODO unsure if needed


# Takes two parameters; dataframe contains the dataset to be split into testing and training datasets, and column is
# the variable that determines the split
def split_dataset_into_train_test(dataframe, column):
    x = dataframe.drop(column, axis=1)
    y = dataframe[column]
    return train_test_split(x, y, test_size=dth.Data.split, random_state=27)


""" 
# Tests the regression model on the currently loaded dataset, prints the predicted results and the actual results for
# simple comparison, prints the mean absoulte error to the console
def regress():
    df = dth.Data.dataframe
    x_train, x_test, y_train, y_test = split_dataset_into_train_test(df, 'years in vivo')

    # Checks if whether a regressor model is saved and the split value hasn't changed
    if dth.load_pickle_file('regressor-model.sav') is not None and Data.split == dth.Data.split:
        regressor = dth.load_pickle_file('regressor-model.sav')
    else:
        regressor = update_regression_model()

    y_pred = regressor.predict(y_test)
    result = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
    mae = metrics.mean_absolute_error(y_test, y_pred)
    print(mae)
    return result, mae
"""


# Function for predicting the longevity of test set. Modify this to work on a singular entry (as with the target
# regress).
def predict_longevity():
    df = prune_features(dth.Data.dataframe)
    x_train, x_test, y_train, y_test = split_dataset_into_train_test(df, 'years in vivo')

    # Checks whether the feature length of the dataset is the same as the model features, retrain model if not
    if dth.load_pickle_file('regressor-model.sav') is not None and Data.split == dth.Data.split:
        regressor = dth.load_pickle_file('regressor-model.sav')
    else:
        regressor = update_regression_model(x_train, y_train)

    # Checks whether the amount of features in the regression model is the same as the data being used to predict a
    # feature. TODO create save-new-model so I don't have to deal with retraining the model every time? Or handle better
    if regressor.max_features_ == len(list(x_test)):
        y_prediction = regressor.predict(x_test)
    else:
        regressor = update_regression_model(x_train, y_train)
        y_prediction = regressor.predict(x_test)

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
    x_train, x_test, y_train, y_test = split_dataset_into_train_test(df, 'years in vivo')

    # Checks whether the feature length of the dataset is the same as the model features, retrain model if not
    if dth.load_pickle_file('regressor-model.sav') is not None and Data.split == dth.Data.split:
        regressor = dth.load_pickle_file('regressor-model.sav')
    else:
        regressor = update_regression_model(x_train, y_train)

    # Checks whether the amount of features in the regression model is the same as the data being used to predict a
    # feature. TODO create save-new-model so I don't have to deal with retraining the model every time? Or handle better
    if regressor.max_features_ == len(list(x_test)):
        y_prediction = regressor.predict(targetpred)
    else:
        regressor = update_regression_model(x_train, y_train)
        y_prediction = regressor.predict(targetpred)

    result = pd.DataFrame({'Actual': target['years in vivo'], 'Predicted': y_prediction})

    # Reshape the arrays to work with R2 score validator
    y_true = y_test.values.reshape(-1, 1)
    r2pred = regressor.predict(x_test)
    r2pred = r2pred.reshape(-1, 1)
    r2 = metrics.r2_score(y_true, r2pred)

    return result, r2


# TESTING FUNCTION - DOES NOT CURRENTLY WORK - USED FOR AUTONOMOUS TESTING OF REGRESSOR PARAMETER TUNING
def masstest(target):
    comparison = [-1000]
    info = dict()

    run = 0
    for a in range(2, 9):
        f = 0.0
        for b in range(2, 12):
            for c in range(2, 20):
                run += 1
                y = 0.0
                regressor = DecisionTreeRegressor(random_state=0)
                r2 = target_predict_longevity(target)
                if r2 > comparison[0]:
                    values = [a, b, c]
                    oof = '%s%s%s%s' % ('run: ', str(run), ' score: ', str(r2))
                    comparison[0] = r2
                    info[oof] = values

                y += 1.0
        f += 1.0

    ''' Test results:
    max_features does best with 2 and 7 (7 max). When < 7, other parameters need to be higher. Best include them all.
    max_depth, min_samples_split and max_leaf_nodes have very little effect
    min_weight_fraction_leaf needs sample weight passed in fit() parameter - no change in my set
    '''
    print(info)


def update_regression_model(x_train, y_train):
    Data.split = dth.Data.split
    
    regressor = DecisionTreeRegressor(random_state=20)
    regressor.fit(x_train, y_train)
    dth.save_file('regressor-model.sav', regressor)
    print('Saved new regression model')
    
    return regressor


# Removes all features from the pandas dataframe that are irrelevant (based on Petes suggestions)
# TODO figure out which values are important?
# TODO check out PCA
def prune_features(df):
    for feature in features_regression:
        df = df.drop(feature, axis=1)
    return df
