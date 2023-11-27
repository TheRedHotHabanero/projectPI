from flask import Flask, flash, request, render_template, session
import os
from werkzeug.utils import secure_filename
import csv
import hashlib
import json


cwd = os.getcwd()
RECEIPT_FOLDER = os.path.join(cwd, 'data/receipt')
CSV_FOLDER = os.path.join(cwd, 'data/certificate')
JSON_FOLDER = os.path.join(cwd, 'data/json')
RESUME_FOLDER = os.path.join(cwd, 'data/resume')
RESUMEJSON_FOLDER = os.path.join(cwd, 'data/resumeJSON')

app = Flask(__name__)
app.secret_key = "parol_losyash"
app.config['RECEIPT_FOLDER'] = RECEIPT_FOLDER
app.config['CSVs'] = CSV_FOLDER
app.config['JSON_FOLDER'] = JSON_FOLDER
app.config['RESUME_FOLDER'] = RESUME_FOLDER
app.config['RESUMEJSON_FOLDER'] = RESUMEJSON_FOLDER


from views import *

if __name__ == "__main__":
	app.run(debug = True)