import sys
import os
from os.path import dirname

module_fix = dirname(os.getcwd())
sys.path.append(module_fix)
for p in sys.path:
    print(p)

print(__name__)

from flask import Flask, render_template
from root.modules import datahandler
from root.modules.ml import ml
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


@app.route('/target', methods=['GET'])
def get_target_prediction_result():
    return test_target_prediction()


@app.route('/')
def index():
    return render_template('index.html')


def mlp_regressor_test():
    predictions, score = ml.mlp_regressor()
    print(score)
    return pandas_to_json(predictions)


def test_regression():
    predictions, r2 = ml.predict_longevity()
    print(r2)
    return pandas_to_json(predictions, r2)


def test_target_prediction():
    test_sample = dth.load_dataframe(dth.Path.path + 'test.csv')
    prediction, r2 = ml.target_predict_longevity(test_sample)
    print(r2)
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
