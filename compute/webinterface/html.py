import os
from flask import Flask, render_template, request
from compute.modules import datahandler
from compute.modules.ml import regressor
from compute.webinterface.nocache import nocache

dth = datahandler

app = Flask(__name__, template_folder='templates')

# Fix for different paths - html.py / main.py
# TODO make it better
dth.Path.pickle_data = '%s%s' % (os.getcwd(), r'/compute/data')
dth.Path.pickle_data = '%s%s' % (os.getcwd(), r'/compute/data')
dataframe = dth.Data.dataframe


# Doesn't work with buttons...yet
@app.route('/', methods=['GET', 'POST'])
@nocache
def index():
    display_dataset()
    if request.method == 'POST':
        if request.form.get('loaddata') == 'loaddata':
            print('load data')
        elif request.form.get('savedata') == 'savedata':
            print('save data')
        elif request.form.get('regress') == 'regress':
            print('regress')
        elif request.form.get('classify') == 'classify':
            print('classify')
    elif request.method == 'GET':
        return render_template('index.html', data=dataframe.to_html())


@app.route('/reload', methods=["POST"])
def load():
    result = regressor.regress(dataframe, dth.Data.split)
    loading_message = 'Loading...'
    return render_template('index.html', message=loading_message, data=result.to_html())


def display_dataset():
    return render_template('index.html', data=dataframe.to_html())


app.run()
