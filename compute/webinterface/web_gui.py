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


@app.route('/save', methods=['GET', 'POST'])
def save_dataframe_as_new():

    return str(dth.save_as_new(dth.Data.dataframe))


@app.route('/regress', methods=['GET'])
def get_regression_result():
    return test_regression()


@app.route('/classify', methods=['GET'])
def get_target_prediction_result():
    dth.Data.split = 0.35
    return test_target_prediction()


@app.route('/')
def index():
    return render_template('index.html')


# This function tests every split value between 0.15 and 0.85, incrementing by 0.01 for every run and running each
# incremental value 15 times. The result is a dictionary containing the split value as key and a list containing the
# resulting R2 scores - pruning out those split values that result in negative R2 score.
def mass_test_split():
    i = 0.15
    r2scores = dict()
    while i < 0.85:
        dth.Data.split = i
        j = 0
        splitvalue_r2score = list()
        while j < 15:
            _, r2 = ml.predict_longevity()
            splitvalue_r2score.append(r2)
            j += 1
        r2scores[i] = splitvalue_r2score
        i += 0.01

    better_scores = r2scores
    for key, values in list(r2scores.items()):
        bad_score = False
        for score in values:
            if score < 0.0:
                bad_score = True
        if bad_score:
            better_scores.pop(key)

    # Prints the value of the better scores dictionary where i represents the split value and better_scores[i]
    # represents the list of r2 scores resulting from that split value
    for i in better_scores:
        print('better_scores: ', i, better_scores[i])

    # Filler code to make the webGUI play nice
    predictions, score = ml.predict_longevity()
    return pandas_to_json(predictions)


def test_regression():
    predictions, score = ml.predict_longevity()
    print(score)
    return pandas_to_json(predictions)


def test_target_prediction():
    test_sample = dth.load_dataframe(dth.Path.path + 'test.csv')
    result = ml.target_predict_longevity(test_sample)
    return pandas_to_json(result)


def test_classification():
    return pandas_to_json(classifier.classify(dth.Data.dataframe))


# Turns a dataframe into a dict, then returns a properly formatted JSON string
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
