from flask import Flask, render_template, request
from compute.modules import dataset

app = Flask(__name__, template_folder='templates')
file = ['df.csv']
defaultdata = dataset.loaddataframe(file[0])


# Doesn't work with buttons...yet
@app.route('/', methods=['GET', 'POST'])
def index():
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
        return render_template('index.html', data=defaultdata.to_html())

    return render_template('index.html', data=defaultdata.to_html())


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


app.run()
