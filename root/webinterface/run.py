import os
from os.path import dirname

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


# TODO add functionality for user input when saving filename - also some kind of "did you just save" check to keep
# TODO people from running scripts on this to save a billion copies and flooding the server
@app.route('/save', methods=['GET', 'POST'])
def save_dataframe_as_new():
    return save_new_dataframe()


@app.route('/mlp', methods=['GET'])
def mlp_regressor():
    return mlp_regressor_test()


@app.route('/regress', methods=['GET'])
def get_regression_result():
    return test_regression()


@app.route('/target', methods=['GET', 'POST'])
def get_target_prediction_result():
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
    return test_target_prediction(None)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/features', methods=['GET', 'POST'])
def select_features():
    return feature_selector()


def mlp_regressor_test():
    result, r2 = ml.mlp_regressor()
    return pandas_to_json(result, r2)


def test_regression():
    predictions, r2 = ml.predict_longevity()
    return pandas_to_json(predictions, r2)


def test_target_prediction(target):
    test_sample = dth.load_dataframe(dth.Path.path + 'test.csv')

    if target is not None:
        prediction, r2 = ml.target_predict_longevity(dth.load_dataframe(target))
        result = pandas_to_json(prediction, r2)
    else:
        prediction, r2 = ml.target_predict_longevity(test_sample)
        result = pandas_to_json(prediction, r2)
    return result


def save_new_dataframe():
    success, filename = dth.save_as_new(dth.Data.dataframe)
    if success:
        feedback = '%s%s%s' % ('<p id="success">success</p><p id="fname">', filename, '</p>')
        return feedback
    else:
        feedback = '%s%s%s' % ('<p id="success">error</p><p id="fname">', 'file was not saved', '</p>')
        return feedback


def feature_selector():
    features = []
    for feature in list(dth.Data.dataframe):
        features.append('<li><input type="checkbox" class="feat" id="' + feature + '" checked="checked"/>' + feature +
                        '</li>')
    return " ".join(features)


# Turns a Pandas dataframe into a dict, then returns a properly formatted JSON string
def pandas_to_json(dataframe, r2score=2):
    if r2score != 2:
        json_result = {'r2': r2score}
        table_data = [dict([(column, row[i]) for i, column in enumerate(dataframe.columns)]) for row in
                      dataframe.values]
        json_result['result'] = table_data
        return json.dumps(json_result)
    else:
        table_data = [dict([(column, row[i]) for i, column in enumerate(dataframe.columns)]) for row in
                      dataframe.values]
        json_result = {'result': table_data}
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
