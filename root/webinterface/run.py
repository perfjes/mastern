import os
import statistics
import pandas as pd
import time
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from modules import datahandler, ml
import json

# Module related variables
dth = datahandler
dth.Data.split = dth.load_split_value_from_pickle()
path = dth.ROOT_DIRECTORY + r'/data/'
dth.Data.dataframe = dth.load_dataframe(path)

# Web app
app = Flask(__name__)

# Testing
r2results = []
prediction_results_list = []


class Data:
    original_features = list(dth.Data.dataframe)
    selected_features = original_features
    recalibrate = False
    stop_process = False


@app.route('/')
def index():
    Data.recalibrate = False
    return render_template('index.html')


@app.route('/dt', methods=['GET'])
def decision_tree_regressor():
    Data.stop_process = False
    start_time = time.time()
    prediction_result = dt_target_prediction()
    end_time = (time.time() - start_time)
    print('Runtime is: ' + str(end_time))

    if Data.recalibrate:
        print(dth.save_results('decision-tree-gridsearchCV', dth.TestData.result_dt))
        params = dth.TestData.result_dt
        for res in params:
            print('Run ' + str(res), params[res])

    return prediction_result


@app.route('/mlp', methods=['GET'])
def mlp_regressor():
    start_time = time.time()
    prediction_result = mlp_target_prediction()
    end_time = (time.time() - start_time)
    print('Runtime is: ' + str(end_time))
    return prediction_result


@app.route('/linear', methods=['GET'])
def linear_regressor():
    start_time = time.time()
    prediction_result = linear_target_prediction()
    end_time = (time.time() - start_time)
    print('Runtime is: ' + str(end_time))
    return prediction_result


@app.route('/features', methods=['GET', 'POST'])
def select_features():
    if request.method == 'GET':
        return feature_selector()
    elif request.method == 'POST':
        features = request.form.getlist('ff')
        print('Features that are saved', features)
        return update_features(features)
    pass


@app.route('/updatetarget', methods=['GET', 'POST'])
def update_target():
    if request.method == 'POST':
        target = request.form.getlist('target')

        if target[-1] == '0':
            target.append(0)
        elif target[-1] == '1':
            target.append(0)
        elif target[-1] == '2':
            target.pop()
            target.append(0)
            target.append(1)
        dth.Data.target = dth.generate_dataframe_from_html(target)
        return str(target)
    pass


@app.route('/science')
def turn_to_science():
    Data.recalibrate = True
    return render_template('science.html')


@app.route('/stopProcess', methods=['POST'])
def cancel():
    Data.stop_process = True
    return 'stopped'


# Decision tree
def dt_target_prediction():
    r2_list = []
    prediction_results_list.clear()

    print('Are we testing?', Data.recalibrate)

    if Data.recalibrate:
        target = dth.load_dataframe('test.csv')
    else:
        target = dth.prune_features(dth.Data.target)
        if target is None:
            print('Target features are too few, what is going on')
            return 'none'

    # FOR ACTUAL USE
    if not Data.recalibrate:
        for x in range(200):
            prediction_result, r2, graphs = ml.target_predict_decision_tree(target, Data.recalibrate)
            r2 = float(r2)
            prediction_results_list.append(float(prediction_result))
            if Data.stop_process:
                print('Process stopped, system made ', len(prediction_results_list), ' predictions')
                break

        prediction = pd.DataFrame(
            {'Actual': target['years in vivo'], 'Predicted': statistics.mean(prediction_results_list)})
        r2_list.append(r2)
        result = format_results_into_json(prediction, statistics.mean(r2_list), graphs)
        get_processed_list_of_predictions(prediction_results_list)

    # FOR TESTING
    else:
        prediction_result, r2, _ = ml.target_predict_decision_tree(target, Data.recalibrate)
        prediction = pd.DataFrame({'Actual': target['years in vivo'], 'Predicted': prediction_result})
        result = format_results_into_json(prediction, r2)

    return result


# Multi-Layer Perceptron
def mlp_target_prediction():
    r2_list = []
    prediction_results_list.clear()

    if Data.recalibrate:
        target = dth.load_dataframe('test.csv')
    else:
        target = dth.Data.target
        if target is None:
            print('Target features are too few, what is going on')
            return 'none'

    # FOR ACTUAL USE
    if not Data.recalibrate:
        for x in range(50):
            prediction_result, r2, graphs = ml.target_predict_mlp(target, Data.recalibrate)
            r2 = float(r2)
            prediction_results_list.append(float(prediction_result))

        prediction = pd.DataFrame(
            {'Actual': target['years in vivo'], 'Predicted': statistics.mean(prediction_results_list)})
        r2_list.append(r2)
        result = format_results_into_json(prediction, statistics.mean(r2_list), graphs)
        get_processed_list_of_predictions(prediction_results_list)

    # FOR TESTING
    else:
        prediction_result, r2, _ = ml.target_predict_mlp(target, Data.recalibrate)
        prediction = pd.DataFrame({'Actual': target['years in vivo'], 'Predicted': prediction_result})
        result = format_results_into_json(prediction, r2)

    return result


# Linear regression
def linear_target_prediction():
    r2_list = []
    prediction_results_list.clear()

    if Data.recalibrate:
        target = dth.load_dataframe('test.csv')
    else:
        target = dth.Data.target
        if target is None:
            print('Target features are too few, what is going on')
            return 'none'

    # FOR ACTUAL USE
    if not Data.recalibrate:
        for x in range(50):
            prediction_result, r2, graphs = ml.target_predict_linear(target, Data.recalibrate)
            r2 = float(r2)
            prediction_results_list.append(float(prediction_result))

        prediction = pd.DataFrame(
            {'Actual': target['years in vivo'], 'Predicted': statistics.mean(prediction_results_list)})
        r2_list.append(r2)
        result = format_results_into_json(prediction, statistics.mean(r2_list), graphs)
        get_processed_list_of_predictions(prediction_results_list)

    # FOR TESTING
    else:
        prediction_result, r2, _ = ml.target_predict_linear(target, Data.recalibrate)
        prediction = pd.DataFrame({'Actual': target['years in vivo'], 'Predicted': prediction_result})
        result = format_results_into_json(prediction, r2)

    return result


# Prints statistics from predictions.
def get_processed_list_of_predictions(results):
    print('Standard deviation: ', statistics.stdev(results))
    print('Maximum years: ', max(results))
    print('Minimum years: ', min(results))
    print('Average years: ', statistics.mean(results))


# Populates a HTML page with a list of checkboxes containing the features (columns) from the dataset.
def feature_selector():
    html_list = ['<form name="feats" action="/features">']
    for feature in Data.original_features:
        if feature != 'case' and feature != 'years in vivo':
            if feature in Data.selected_features and feature not in dth.Features.initially_deactivated:
                html_list.append(
                    '<li class="featureSelector"><input type="checkbox" name="ff" class="feat" value="' + feature +
                    '" checked="checked"/>' + feature + '</li>')
            else:
                html_list.append(
                    '<li class="featureSelector"><input type="checkbox" name="ff" class="feat" value="' + feature +
                    '"/>' + feature + '</li>')
    html_list.append('</form>')

    return " ".join(html_list)


# Gets all features from the feature selection page, filters out the deselected features (on the page) from the dataset.
def update_features(features):
    Data.selected_features = features

    for feature in Data.original_features:
        if feature in Data.selected_features and feature in dth.Features.drop_features_regression:
            dth.Features.drop_features_regression.remove(feature)
        if feature != 'years in vivo' and feature != 'case':
            if feature not in Data.selected_features and feature not in dth.Features.drop_features_regression:
                dth.Features.drop_features_regression.append(feature)

    print('Drop features: ', dth.Features.drop_features_regression)
    dth.Data.target = dth.prune_features(dth.Data.target)
    print('target features: ', list(dth.Data.target))
    return feature_selector()


# Dataframe, R2 score and a list of graphs are passed and the function returns a dict formatted into a proper JSON
# string.
def format_results_into_json(dataframe, r2score=None, graphs=list()):
    json_result = {}
    if r2score is not None:
        json_result['r2'] = r2score

    json_result['graphs'] = graphs

    print(graphs)

    table_data = [dict([(column, row[i]) for i, column in enumerate(dataframe.columns)]) for row in
                  dataframe.values]
    json_result['result'] = table_data

    return json.dumps(json_result)


# Attempt at fixing Chrome overaggressive caching. It work.
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 0 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == "__main__":
    app.run(debug=True)
