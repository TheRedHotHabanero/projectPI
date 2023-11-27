from flask import Flask, flash, request, render_template, session
import os
from werkzeug.utils import secure_filename
import csv
import hashlib
import json


cwd = os.getcwd()
CSVS = os.path.join(cwd, 'data/University_CSVs')
JSON_KEYS = os.path.join(cwd, 'data/JSON_keys')

app = Flask(__name__)
app.secret_key = "parol_losyash"
app.config['CSVs'] = CSVS
app.config['JSONs'] = JSON_KEYS


@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('home.html')


if __name__ == "__main__":
	app.run(debug = True)