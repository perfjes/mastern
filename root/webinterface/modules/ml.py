from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neural_network.multilayer_perceptron import MLPRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, LeaveOneOut
from sklearn import metrics
from modules import datahandler, graph_factory
import numpy as np
import statsmodels.api as sm

dth = datahandler
graph = graph_factory


class Data:
    arthroplasty_dataset = list(dth.load_dataframe('db.csv'))  # the original file TODO probs useless
    dataset_features = list(dth.Data.dataframe)
    dt_regressor = dth.load_file('dt-regressor.sav')
    mlp_regressor = dth.load_file('mlp-regressor.sav')
    recalibrate = False


# Splits the dataset into two parts - one for training, one for testing, with a split of 65% of the dataset used for
# training and the remaining 35% for testing. Returns training and testing data to be fitted by the model.
# In order to ensure that a certain amont of test case subjects from the dataset (the first 20 or so) are evenly split
def split_dataset_into_train_test(dataframe, column, recalibrate=False):
    x = dataframe.drop(column, axis=1)
    y = dataframe[column]

    # Create a training/testing split
    if recalibrate:
        print('recalibrate is turned on')
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.35, random_state=33)
    else:
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.35)

    # TODO might not be necessary - just in case there's too little or too much of control cases in the
    # TODO training/testing subset. Not optimal by any means, just a temporary solution.
    while (len(x.loc[x['case'] == 0].index) / 2.2) > len(x_train.loc[x_train['case'] == 0].index) > \
            len(x.loc[x['case'] == 0].index) / 1.5:
        print('\n', 'RECALIBRATING', '\n')
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.35)

    return x_train, x_test, y_train, y_test


def float_test():
    float_list = []
    x = 0.01
    y = 1.0
    while x < y:
        float_list.append(x)
        x += 0.01
    return float_list


# Loads a previously saved regression model if there is one, trains a new if there's not. If the dataframe being used
#  for the prediction have more or less features than the regression model,
def validate_or_create_regressor(filename):
    df = dth.prune_features(dth.Data.dataframe)
    x_train, x_test, y_train, y_test = split_dataset_into_train_test(df, 'years in vivo')

    if dth.load_file(filename) is not None:
        regressor = dth.load_file(filename)
    else:
        regressor = update_regression_model(filename, x_train, y_train)

    # Checks whether the amount of features in the regression model is the same as the data being used to predict a
    # feature. TODO create save-new-model so I don't have to deal with retraining the model every time? Or handle better
    if filename != 'mlp-regressor.sav':
        if regressor.max_features_ == len(list(x_test)):
            return regressor
        else:
            regressor = update_regression_model(filename, x_train, y_train)
            return regressor
    else:
        regressor = update_regression_model(filename, x_train, y_train)
        return regressor


def update_regression_model(filename, x_train, y_train):
    if filename == 'dt-regressor.sav':
        regressor = DecisionTreeRegressor(criterion='friedman_mse', max_depth=12, min_samples_split=13, splitter='random',
                                          max_leaf_nodes=18, min_impurity_decrease=0.08, presort=False)
        regressor.fit(x_train, y_train)
        dth.save_file(filename, regressor)
        print('Saved new regression model as', filename)
        return regressor
    elif filename == 'mlp-regressor.sav':
        regressor = MLPRegressor(activation='tanh', alpha=0.001, early_stopping=True, hidden_layer_sizes=(25, 20, 40),
                                 solver='lbfgs', max_iter=100)
        regressor.fit(x_train, y_train)
        dth.save_file(filename, regressor)
        print('Saved new regression model as', filename)
        return regressor
    elif filename == 'linear-regressor.sav':
        regressor = LinearRegression(fit_intercept=True, normalize=True, copy_X=True)
        regressor.fit(x_train, y_train)
        dth.save_file(filename, regressor)
        print('Saved new regression model as', filename)
        return regressor
    else:
        print('Wrong filetype?')


# Function for predicting the longevity of a single sample - given the training/testing dataset and a new CSV file
# containing the exact same features as the training/testing set.
def target_predict_decision_tree(target, recalibrate=False, count=0):
    x_train, x_test, y_train, y_test = split_dataset_into_train_test(dth.prune_features(dth.Data.dataframe),
                                                                     'years in vivo', recalibrate)
    if 'years in vivo' not in target:
        return False, False, False

    target_pred = target.drop('years in vivo', axis=1)

    if recalibrate:
        parameters = {
            'criterion': ('mse', 'friedman_mse', 'mae'),
            # 'splitter': ('best', 'random'),
            # 'max_depth': (3, 5, 8, 12, 16, 18, 22),
            # 'min_samples_split': (2, 3, 4, 5, 6, 9, 11, 16, 21, 25),
            # 'max_leaf_nodes': range(4, 15),
            # 'min_impurity_decrease': (0.0, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.2),
            'presort': (True, False),
            # 'random_state': range(0, 101)
        }

        regressor = GridSearchCV(DecisionTreeRegressor(criterion='mae', max_depth=8, min_samples_split=8,
                                                       splitter='best', max_leaf_nodes=15, min_impurity_decrease=0.0,
                                                       presort=True, random_state=83), parameters, n_jobs=-1)

        regressor.fit(x_train, y_train)
        print(regressor.best_params_)
        print('R2 is: ' + str(regressor.best_score_))
        dth.save_file('DTRegressionBestParams.sav', regressor.best_params_)
        r2 = str(regressor.best_score_)

    else:
        regressor = validate_or_create_regressor('dt-regressor.sav')
        regressor.fit(x_train, y_train)

    r2_prediction = regressor.predict(x_test)
    prediction = regressor.predict(target_pred)

    if recalibrate:
        dth.TestData.result_dt[str(count)] = {"R2": str(regressor.best_score_), "prediction": str(prediction[0]),
                                               "parameters": regressor.best_params_}
    else:
        y_true = y_test.values.reshape(-1, 1)
        r2_pred = r2_prediction.reshape(-1, 1)
        r2 = metrics.r2_score(y_true, r2_pred)

    return prediction, r2, make_some_graphs()


def target_predict_mlp(target, recalibrate=False, count=0):
    x_train, x_test, y_train, y_test = split_dataset_into_train_test(dth.prune_features(dth.Data.dataframe),
                                                                     'years in vivo', recalibrate=False)
    target_pred = target
    target_pred = target_pred.drop('years in vivo', axis=1)

    if recalibrate:
        parameters = {
            # 'hidden_layer_sizes': [x for x in itertools.product((10, 15, 20, 25, 30, 40, 45, 50, 55, 60), repeat=1)],
            # 'hidden_layer_sizes': [x for x in itertools.product((10, 20, 25, 30, 40, 45, 50, 55, 60), repeat=3)],
            # 'hidden_layer_sizes': [x for x in itertools.product((10, 20, 30, 40, 50, 60, 70, 80), repeat=4)],
            'activation': ('identity', 'logistic', 'tanh', 'relu'),
            # 'max_iter': range(100, 300),
            'alpha': (0.0000, 0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008, 0.001, 0.0015, 0.0025),
            'early_stopping': (True, False)
        }
        regressor = GridSearchCV(MLPRegressor(activation='tanh', alpha=0.001, early_stopping=True,
                                              hidden_layer_sizes=(25, 20, 40), solver='lbfgs', max_iter=100,
                                              random_state=22), parameters, n_jobs=-1)

        regressor.fit(x_train, y_train)
        print(regressor.best_params_)
        print('R2 is: ' + str(regressor.best_score_))
        dth.save_file('MLPRegressionBestParams.sav', regressor.best_params_)
        r2 = regressor.best_score_
    else:
        regressor = validate_or_create_regressor('mlp-regressor.sav')
        regressor.fit(x_train, y_train)

    r2_prediction = regressor.predict(x_test)
    prediction = regressor.predict(target_pred)

    if recalibrate:
        dth.TestData.result_dt[str(count)] = {"R2": str(regressor.best_score_), "prediction": str(prediction[0]), "parameters": regressor.best_params_}
    else:
        y_true = y_test.values.reshape(-1, 1)
        r2_pred = r2_prediction.reshape(-1, 1)
        r2 = metrics.r2_score(y_true, r2_pred)

    return prediction, r2, make_some_graphs()


def target_predict_linear(target, recalibrate=False, count=0):
    target_pred = target.drop('years in vivo', axis=1)
    x_train, x_test, y_train, y_test = split_dataset_into_train_test(dth.prune_features(dth.Data.dataframe),
                                                                     'years in vivo', recalibrate=False)
    if recalibrate:
        parameters = {
            'fit_intercept': (True, False),
            'normalize': (True, False),
            'copy_X': (True, False)
        }

        regressor = GridSearchCV(LinearRegression(), parameters, n_jobs=-1)
        regressor.fit(x_train, y_train)
        print(regressor.best_params_)
        print('R2 is: ' + str(regressor.best_score_))
        dth.save_file('LinearRegressionBestParams.sav', regressor.best_params_)
        r2 = regressor.best_score_
    else:
        regressor = LinearRegression()
        regressor.fit(x_train, y_train)

    r2_prediction = regressor.predict(x_test)
    prediction = regressor.predict(target_pred)

    if recalibrate:
        dth.TestData.result_dt[str(count)] = {"R2": str(regressor.best_score_), "prediction": str(prediction[0]),
                                              "parameters": regressor.best_params_}
    else:
        y_true = y_test.values.reshape(-1, 1)
        r2_pred = r2_prediction.reshape(-1, 1)
        r2 = metrics.r2_score(y_true, r2_pred)

    return prediction, r2, make_some_graphs()


def make_some_graphs():
    graphs = []
    count = 1
    for feature in list(dth.Data.dataframe):

        if feature != 'years in vivo':
            graphs.append(graph.generate_graph(dth.Data.dataframe['years in vivo'], dth.Data.dataframe[feature],
                                               'years in vivo', feature, 'Relation between longevity and ' + feature,
                                               'graph' + str(count) + '.png'))
            count += 1

    return graphs


def leave_one_out(twenty=False):
    if twenty:
        data = dth.prune_features(dth.Data.dataframe.head(20))
        print(data)
    else:
        data = dth.prune_features(dth.Data.dataframe)
    targets = np.array(data['years in vivo'])
    dataset = np.array(data.drop('years in vivo', axis=1))

    loo = LeaveOneOut()
    ytests, ypreds, r2yt, r2yp = [], [], [], []

    for train, test in loo.split(dataset):
        x_train, x_test = dataset[train], dataset[test]
        y_train, y_test = targets[train], targets[test]

        regressor = DecisionTreeRegressor(criterion='friedman_mse', max_depth=12, min_samples_split=13,
                                          splitter='random', max_leaf_nodes=18, min_impurity_decrease=0.08,
                                          presort=False, random_state=13)
        regressor.fit(x_train, y_train)
        prediction = regressor.predict(x_test)

        r2yt.append(y_test)
        r2yp.append(prediction)
        ytests.append(float(y_test))
        ypreds.append(float(prediction))

    r2 = metrics.r2_score(r2yt, r2yp)

    return ytests, ypreds, r2


def multiple_regression_analysis(twenty=False):
    if twenty:
        data = dth.prune_features(dth.Data.dataframe.head(20))
    else:
        data = dth.prune_features(dth.Data.dataframe)

    X = data['linwear']
    y = data['years in vivo']

    model = sm.OLS(y, X).fit()
    predictions = model.predict(X)
    print('PREDICTIONS ', predictions)

    graphs = [graph.generate_graph(X, y, 'Linear Wear', 'Years in Vivo', 'Yikes', 'mlr_graph.png')]

    model.summary()
    return predictions
