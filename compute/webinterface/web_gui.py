from io import StringIO

from flask import Flask, render_template, Blueprint, request
from compute.modules import datahandler
from compute.modules.ml import regressor, classifier
from flask_restful import Api, Resource
import json
import pandas as pd

# Module related variables
dth = datahandler
dth.Data.split = dth.load_split_value_from_pickle()
path = dth.ROOT_DIRECTORY + r'/data/'
dth.Data.dataframe = dth.load_dataframe(path)

# Web app
app = Flask(__name__)
api_blueprint = Blueprint('api', __name__)
web_api = Api(api_blueprint)


class Data(Resource):
    def get(self):
        return dth.Data.dataframe.to_json()


@app.route('/regress', methods=['GET', 'POST'])
def get_regression_result():
    return test_regression()


@app.route('/classify', methods=['GET', 'POST'])
def get_classification_result():
    return test_classification()


@app.route('/split', methods=['GET', 'POST'])
def get_split_input_from_html():
    dth.Data.split = float(request.form['split'])
    print(dth.Data.split)
    print(type(dth.Data.split))
    return render_template('index.html', split=dth.Data.split)


# Doesn't work with buttons...yet
@app.route('/')
def index():
    # Initiate website
    return render_template('index.html', split=dth.Data.split)


def test_regression():
    ohno, nope = regressor.regress(dth.Data.dataframe)
    return pandas_to_json(ohno)


def test_classification():
    result = classifier.classify(dth.Data.dataframe)
    print(result)
    print(type(result))
    return pandas_to_json(result)


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


web_api.add_resource(Data, '/api/data/<string:file>', endpoint='data')

if __name__ == "__main__":
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.run(debug=True)
