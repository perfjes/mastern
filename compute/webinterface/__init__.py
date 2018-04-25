import os
from flask import Flask

app = Flask(__name__)
app._static_folder = os.path.abspath("webinterface/static/main.static")
app.debug = True