from io import StringIO

from flask import Flask, render_template, Blueprint
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


# Doesn't work with buttons...yet
@app.route('/')
def index():
    # Initiate website
    return render_template('index.html')


def test_regression():
    ohno, nope = regressor.regress(dth.Data.dataframe, dth.Data.split)
    return pandas_to_json(ohno)


def test_classification():
    result = StringIO(classifier.classify(dth.Data.dataframe))
    resulty = pandas_to_json(pd.read_csv(result, sep=' '))
    return resulty


def pandas_to_json(df):
    d = [
        dict([
            (colname, row[i])
            for i,colname in enumerate(df.columns)
        ])
        for row in df.values
    ]

    boi = {'result':d}
    return json.dumps(boi)


# Attempt at fixing Chrome overaggressive caching
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
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
