from flask import Flask, flash, request, render_template, session
import os
from werkzeug.utils import secure_filename
import csv
import hashlib
import json

# from merkletools import MerkleTools
# from blockchain import Blockchain


cwd = os.getcwd()
CSVS = os.path.join(cwd, 'data/University_CSVs')
JSON_KEYS = os.path.join(cwd, 'data/JSON_keys')

app = Flask(__name__)
app.secret_key = "parol_losyash"
app.config['CSVs'] = CSVS
app.config['JSONs'] = JSON_KEYS


@app.route('/', methods=['GET'])
def home():
	return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	passwords = {}

	with open("passwords.json") as f:
		passwords = json.loads(f.read())

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if username not in passwords.keys():
			flash("University not registered", "error")
			return render_template('login.html')
		if passwords[username] != hashlib.sha3_256(password.encode()).hexdigest():
			flash("Authorization failed. Try again.", "error")
			return render_template('login.html')	
		session['logged_in'] = True
		session['username'] = username
		return render_template('upload.html')
	return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():

	if request.method == 'POST':
		if 'file' not in request.files:
			flash("No file selected", "error")
			error = "No file selected"
			return render_template('upload.html', error = error)
		file = request.files['file']
		if file.filename == '':
			flash("No file selected", "error")
			return render_template('upload.html')
		
		if file and file.filename.split(".")[-1] == 'csv':
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['CSVs'], filename))
			mt = MerkleTools(hash_type='sha3_256')
			count = 0

			with open(os.path.join(app.config['CSVs'], filename)) as f:  
				reader = csv.reader(f)
				for row in reader:
					#studentID CPI Name batch college
					data = str(row[0]) + str(row[2]) + str(row[1]) + str(row[3]) + session['username']
					year_batch = str(row[3])
					mt.add_leaf(data, do_hash= True)
					count += 1

			mt.make_tree()
			if mt.get_tree_ready_state:
				merkleRoot = mt.get_merkle_root()
			
			institute = session['username']
			bc = Blockchain(institute)
			print("Adding to the blockchain: ", session['username'], year_batch, merkleRoot)
			try:
				bc.addBatchMerkleRoot(year_batch, merkleRoot)
			except:
				error = "Institute not registered!"
				return render_template('upload.html', error=error)

			itr = 0

			with open(os.path.join(app.config['CSV_FOLDER'], filename)) as File:  
				reader = csv.reader(File)
				for row in reader:
					data={}
					data["cpi"] = str(row[2])
					data["name"] = str(row[1])
					data["year"] = str(row[3])
					data["studentId"] = str(row[0])
					data["institution"] = session['username']
					data["merklePath"] = mt.get_proof(itr)
					itr += 1

					filename = str(row[1]) + '.json'

					with open(os.path.join(app.config['JSONs'], filename), 'w') as json_file:
						json_file.write(json.dumps(data))
					
				flash("Information successfully added.", "success")

		else:
			flash("Please, check uploaded file. It should be .csv format.", "error")
			error = "Wrong file"
			return render_template('upload.html', error = error)
					
	return render_template('upload.html')


@app.route('/verify', methods=['GET', 'POST'])
def verify():

	if request.method == 'POST':
		if 'file' not in request.files:
			flash("No file selected", "error")
			error = "No file selected"
			return render_template('verify.html', error = error)
		
		jsonFile = request.files['json']
		if jsonFile.filename == '':
			flash("No file selected", "error")
			return render_template('verify.html')
		
		if jsonFile and jsonFile.filename.split(".")[-1] == 'json':

			json_name = secure_filename(jsonFile.filename)
			jsonFile.save(os.path.join(app.config['JSONs'], json_name))
			
			with open(os.path.join(app.config['JSONs'], json_name)) as receiptJson:
				receiptJsonData = json.loads(receiptJson.read())

			mt = MerkleTools(hash_type='sha3_256')
			data = receiptJsonData['studentId'] + receiptJsonData['cpi'] + receiptJsonData['name'] + receiptJsonData['year'] + receiptJsonData['institution']
			data = data.encode()
			data = hashlib.sha3_256(data).hexdigest()

			merkleRoot = mt.validate_proof(receiptJsonData['merklePath'], data)
			res = False
			try:
				bc = Blockchain("VJTI")
				res = bc.verifyBatchMerkleRoot(receiptJsonData["institution"], receiptJsonData["year"], merkleRoot)
			except:
				print("Error occurred")
			if res is True:
				flash(f"Data about diploma found:\nName:{receiptJsonData['name']}\nUniversity:{receiptJsonData['institution']}\nGraduation year:{receiptJsonData['year']}", "success")
			else:
				flash("JSON key seems to be depricated or fake.", "error")
		else:
			flash("Please, check uploaded file. It should be .json format.", "error")
			error = "Wrong file"
			return render_template('verify.html', error = error)

	return render_template('verify.html')





if __name__ == "__main__":
	app.run(debug = True)