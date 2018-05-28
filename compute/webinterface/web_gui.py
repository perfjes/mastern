import os
from flask import Flask, render_template, request
from compute.modules import datahandler
from compute.modules.ml import regressor
from compute.webinterface.nocache import nocache

dth = datahandler

app = Flask(__name__, template_folder='templates')

# Fix for different paths - web_gui.py / main.py
# TODO make it better
dth.Path.pickle_data = '%s%s' % (os.getcwd(), r'/compute/data')
dth.Path.pickle_data = '%s%s' % (os.getcwd(), r'/compute/data')
dataframe = dth.Data.dataframe


app.config['CACHE_TYPE'] = 'null'


# Doesn't work with buttons...yet
@app.route('/', methods=['GET', 'POST'])
@nocache
def index():
    if request.method == 'POST':
        if request.form.get('loaddata') == 'loaddata':
            print('load data')
            return render_dataset()
        elif request.form.get('savedata') == 'savedata':
            print('save data')
            return render_dataset()
        elif request.form.get('regress') == 'regress':
            print('regress')
            return render_dataset()
        elif request.form.get('classify') == 'classify':
            print('classify')
            return render_dataset()
    elif request.method == 'GET':
        return render_template('index.html', data=dataframe.to_html())


def render_dataset():
    return render_template('index.html', data=dataframe.to_html())


@app.route('/reload', methods=["POST"])
@nocache
def load():
    result = regressor.regress(dataframe, dth.Data.split)
    loading_message = 'Loading...'
    return render_template('index.html', message=loading_message, data=result.to_html())


app.run()
