from flask import Flask, render_template, Blueprint, request
from compute.modules import datahandler
from compute.modules.ml import classifier, ml
from flask_restful import Api, Resource
import json

# Module related variables
dth = datahandler
dth.Data.split = dth.load_split_value_from_pickle()
path = dth.ROOT_DIRECTORY + r'/data/'
dth.Data.dataframe = dth.load_dataframe(path)

# Web app
app = Flask(__name__)


# Maybe delegating the code snippet to a separate function will help - it doesn't do much right now
@app.route('/save', methods=['GET', 'POST'])
def save_dataframe_as_new():
    return save_new_dataframe()


@app.route('/regress', methods=['GET'])
def get_regression_result():
    return test_regression()


@app.route('/target', methods=['GET'])
def get_target_prediction_result():
    return test_target_prediction()


@app.route('/')
def index():
    return render_template('index.html')


def test_regression():
    predictions, score = ml.predict_longevity()
    print(score)
    return pandas_to_json(predictions)


def test_target_prediction():
    test_sample = dth.load_dataframe(dth.Path.path + 'test.csv')
    prediction, r2 = ml.target_predict_longevity(test_sample)
    result = pandas_to_json(prediction)
    return result


def test_classification():
    return pandas_to_json(classifier.classify(dth.Data.dataframe))


def save_new_dataframe():
    success, filename = dth.save_as_new(dth.Data.dataframe)
    if success:
        feedback = '%s%s%s' % ('<p id="success">success</p><p id="fname">', filename, '</p>')
        return feedback
    else:
        feedback = '%s%s%s' % ('<p id="success">error</p><p id="fname">', 'file was not saved', '</p>')
        return feedback


# Turns a Pandas dataframe into a dict, then returns a properly formatted JSON string
def pandas_to_json(dataframe):
    json_result = [
        dict([
            (column, row[i])
            for i, column in enumerate(dataframe.columns)
        ])
        for row in dataframe.values
    ]
    return json.dumps({'result': json_result})


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
