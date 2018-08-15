import datetime
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


# TODO add functionality for user input when saving filename - also some kind of "did you just save" check to keep
# TODO people from running scripts on this to save a billion copies and flooding the server
@app.route('/save', methods=['GET', 'POST'])
def save_dataframe_as_new():
    return save_new_dataframe()
# TODO maybe just remove this :)


@app.route('/dt', methods=['GET', 'POST'])
def decision_tree_regressor():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        name = file.filename.split('/')
        print(name)
        if file and name[(len(name) - 1)].lower().endswith('.csv'):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))

    start_time = time.time()
    prediction_result = dt_target_prediction()
    end_time = (time.time() - start_time)
    print('Runtime is: ' + str(end_time))

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
    dth.save_file(('results' + st + '.json'), dth.Test_data.result_dt)
    params = dth.Test_data.result_dt
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


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/features', methods=['GET', 'POST'])
def select_features():
    if request.method == 'GET':
        return feature_selector()
    elif request.method == 'POST':
        features = request.form.getlist('ff')
        print('Features that are saved', features)
        return update_features(features)
    pass


# TODO implement multiple runs if recalibrate is turned off - gather results of each run, present
# best/worst/mean/standard deviation
# Decision tree
def dt_target_prediction():
    prediction_results_list.clear()
    target = dth.load_dataframe(dth.Path.path + 'test.csv')
    if not Data.recalibrate:
        for x in range(1500):
            prediction_result, r2 = ml.target_predict_decision_tree(target, Data.recalibrate)
            prediction = pd.DataFrame({'Actual': target['years in vivo'], 'Predicted': prediction_result})
            result = pandas_to_json(prediction, r2)
            prediction_results_list.append(float(prediction_result))
        get_processed_list_of_predictions(prediction_results_list)
    else:
        for x in range(5):  # FOR TESTING
            prediction_result, r2 = ml.target_predict_decision_tree(target, Data.recalibrate, x)
            prediction = pd.DataFrame({'Actual': target['years in vivo'], 'Predicted': prediction_result})
            result = pandas_to_json(prediction, r2)

    return result


# Multi-Layer Perceptron
def mlp_target_prediction():
    prediction_results_list.clear()
    target = dth.load_dataframe(dth.Path.path + 'test.csv')
    if not Data.recalibrate:
        for x in range(50):
            prediction_result, r2 = ml.target_predict_mlp(target, Data.recalibrate)
            prediction = pd.DataFrame({'Actual': target['years in vivo'], 'Predicted': prediction_result})
            result = pandas_to_json(prediction, r2)
            prediction_results_list.append(float(prediction_result))
        get_processed_list_of_predictions(prediction_results_list)
    else:
        prediction_result, r2 = ml.target_predict_mlp(target, Data.recalibrate)
        prediction = pd.DataFrame({'Actual': target['years in vivo'], 'Predicted': prediction_result})
        result = pandas_to_json(prediction, r2)

    return result


# Linear regression
def linear_target_prediction():
    prediction_results_list.clear()
    target = dth.load_dataframe(dth.Path.path + 'test.csv')
    if not Data.recalibrate:
        for x in range(500):
            prediction_result, r2 = ml.target_predict_linear(target, Data.recalibrate)
            prediction_results_list.append(float(prediction_result))
            prediction = pd.DataFrame({'Actual': target['years in vivo'], 'Predicted': prediction_result})
            result = pandas_to_json(prediction, r2)
        get_processed_list_of_predictions(prediction_results_list)
    else:
        prediction_result, r2 = ml.target_predict_linear(target, Data.recalibrate)
        prediction = pd.DataFrame({'Actual': target['years in vivo'], 'Predicted': prediction_result})
        result = pandas_to_json(prediction, r2)

    return result


def get_processed_list_of_predictions(results):
    print(results)
    print('Standard deviation: ', statistics.stdev(results))
    print('Maximum years: ', max(results))
    print('Minimum years: ', min(results))
    print('Average years: ', statistics.mean(results))


# TODO deprecated
def save_new_dataframe():
    success, filename = dth.save_as_new(dth.Data.dataframe)
    if success:
        feedback = '%s%s%s' % ('<p id="success">success</p><p id="fname">', filename, '</p>')
        return feedback
    else:
        feedback = '%s%s%s' % ('<p id="success">error</p><p id="fname">', 'file was not saved', '</p>')
        return feedback


def feature_selector():
    html_list = ['<form name="feats" action="/features" methods="POST">']
    for feature in Data.original_features:
        if feature != 'case' and feature != 'years in vivo':
            if feature in Data.selected_features and feature not in dth.Features.initially_deactivated:
                html_list.append('<li><input type="checkbox" name="ff" class="feat" value="' + feature + '" checked="checked"/>' +
                        feature + '</li>')
            else:
                html_list.append('<li><input type="checkbox" name="ff" class="feat" value="' + feature + '"/>' + feature + '</li>')
    html_list.append('</form>')

    return " ".join(html_list)


def update_features(features):
    Data.selected_features = features
    for feature in Data.original_features:
        if feature in Data.selected_features and feature in dth.Features.drop_features_regression:
            dth.Features.drop_features_regression.remove(feature)
        if feature != 'years in vivo' and feature != 'case':
            if feature not in Data.selected_features and feature not in dth.Features.drop_features_regression:
                dth.Features.drop_features_regression.append(feature)
    print('Drop features: ', dth.Features.drop_features_regression)
    dth.Data.dataframe = dth.load_dataframe('df.csv')
    print('Dataframe columns: ', list(dth.Data.dataframe))
    return feature_selector()


# Turns a Pandas dataframe into a dict, then returns a properly formatted JSON string
def pandas_to_json(dataframe, r2score=2):
    json_result = {}
    if r2score != 2:
        json_result['r2'] = r2score

    table_data = [dict([(column, row[i]) for i, column in enumerate(dataframe.columns)]) for row in
                  dataframe.values]
    json_result['result'] = table_data

    return json.dumps(json_result)


# Attempt at fixing Chrome overaggressive caching
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
