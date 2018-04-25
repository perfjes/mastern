import os
from flask import Flask, render_template, url_for
from compute.modules import dataset, regressor, classifier

app = Flask(__name__, template_folder='templates')
file = ['df.csv']
defaultdata = dataset.loaddataframe(file[0])


@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html', data=defaultdata.to_html())

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

app.run()
