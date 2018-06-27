import csv

from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn import metrics
from compute.modules import datahandler, graph_factory

dth = datahandler
graph = graph_factory

drop_features_regression = ['id', 'case', 'cuploose', 'stemloose', 'volwear', 'volwearrate', 'cupx', 'cupy', 'zr', 'ni']  # These are removed

"""
    List of all features in the dataset
    'id', 'case', 'cuploose', 'stemloose', 'years in vivo', 'cr', 'co', 'zr', 'ni', 'mb', 'linwear', 'linwearrate', 
    'volwear', 'volwearrate', 'inc', 'ant', 'cupx', 'cupy', 'male', 'female'
    
"""


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
    return train_test_split(x, y, test_size=0.33, random_state=0)


# Function for predicting the longevity of test set. Modify this to work on a singular entry (as with the target
# regress).
def predict_longevity():
    x_train, x_test, y_train, y_test, regressor = validate_regression_model()
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
    target = prune_features(target)
    targetpred = target.drop('years in vivo', axis=1)

    # Actual prediction
    x_train, x_test, y_train, y_test, regressor = validate_regression_model()
    y_prediction = regressor.predict(targetpred)
    result = pd.DataFrame({'Actual': target['years in vivo'], 'Predicted': y_prediction})

    # Reshape the arrays to work with R2 score validator
    y_true = y_test.values.reshape(-1, 1)
    r2_pred = regressor.predict(x_test)
    r2_pred = r2_pred.reshape(-1, 1)
    r2 = metrics.r2_score(y_true, r2_pred)

    features = list(targetpred)
    i = 0
    importances = dict()
    for value in regressor.feature_importances_:
        importances[features[i]] = value
        i += 1

    for key, value in importances.items():
        print(key, value)

    return result, r2


# Loads a previously saved regression model if there is one, trains a new if there's not. If the dataframe being used
#  for the prediction have more or less features than the regression model,
def validate_regression_model():
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
        return x_train, x_test, y_train, y_test, regressor
    else:
        regressor = update_regression_model(x_train, y_train)
        return x_train, x_test, y_train, y_test, regressor


def update_regression_model(x_train, y_train):
    Data.split = dth.Data.split
    
    regressor = DecisionTreeRegressor(max_depth=2, random_state=0)
    regressor.fit(x_train, y_train)
    # dth.save_file('regressor-model.sav', regressor)  TODO activate to save again
    print('Saved new regression model')
    
    return regressor


# Removes all features from the pandas dataframe that are irrelevant (based on Petes suggestions)
# TODO figure out which values are important?
# TODO check out PCA
def prune_features(df):
    for feature in drop_features_regression:
        df = df.drop(feature, axis=1)
    return df


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
