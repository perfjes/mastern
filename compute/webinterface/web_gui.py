import os
from flask import Flask, render_template, request
from compute.modules import datahandler
from compute.modules.ml import regressor

dth = datahandler
dth.Data.dataframe = dth.load_dataframe_from_pickle()
dth.Data.split = dth.load_split_value_from_pickle()

app = Flask(__name__)

# Fix for different paths - web_gui.py / main.py
# TODO make it better

path = dth.ROOT_DIRECTORY + r'/data/'


def test_regression():
    dth.Data.dataframe = dth.load_dataframe(path)
    ohno, nope = regressor.regress(dth.Data.dataframe, dth.Data.split)
    return render_template('index.html', data=ohno.sort_index().to_html())


# Doesn't work with buttons...yet
@app.route('/')
def index():

    return test_regression()
    # return render_template('index.html', data=dth.load_dataframe(path).to_html())


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


if __name__ == "__main__":
    app.run(debug=True)
