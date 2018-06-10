"""
	Import External Libs
"""
from flask import Flask, render_template, Response, flash, redirect, request, session, abort, url_for;
from werkzeug.utils import secure_filename;
import sys, os;
import flask;
import json;
import datetime;

sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'analytics_modules/')));
from CompressManager import *;

# This is where we save uploaded  files
UPLOAD_FOLDER = './UploadFiles/';
# The only file extension we will allow is txt, as indicated by the instructions.
ALLOWED_EXTENSIONS = set(['jpg'])



# Creating flask app
app = Flask(__name__);
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



"""
	This the end-point for the main (root) page.
"""
@app.route("/")
def LandingPage():
	# On-root load, the msg is none.
	msg = {"msg":"none"}
	# Render the landingpage html page.
	return render_template('landingPage.html', msg=msg)


"""
	This function is used for checking the allowed extension of the upload files.
"""
def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


"""
	API end-point for uploading  txt files.
	POST -> As indicated by the instructions, it takes file input (txt).
	GET  -> This call will return the landing page. 
"""
@app.route("/uploadfile", methods=['GET','POST'])
def UploadFile():
	# Create a msg object
	msg = {};
	# Check if the request is POST or GET.
	if(request.method == 'POST'):
		compression_rate_x = request.form["compression_rate_x"];
		compression_rate_y = request.form["compression_rate_y"];
		
		# Check if the file exists in the request
		if 'file' not in request.files:
			# If not, return to landing page with msg, indicating that the use must add a file
			# to the form.
			msg["msg"] = "Please upload a  file.";
			return render_template('landingPage.html', msg=msg)

		# Grab the file from the request object
		file = request.files['file']
		# Double check if the file is attached correctly and raise user error, if not.
		if file.filename == '':
			msg["msg"] = "Please upload a  file.";
			return render_template('landingPage.html', msg=msg)

		# Check to make sure the file uploaded is txt
		if file and allowed_file(file.filename):
			# Create a file name, based on time/date of file upload.
			filename = "UploadFile_"+str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"));
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename+".jpg"));
			
			status = Compress(filename,compression_rate_x,compression_rate_y);
			if(status):
				msg["msg"] = "pass";
				msg["file_name"] = str(filename);		
				return render_template('landingPage.html', msg=msg);
			else:
				msg["msg"] = "Error while performing compression.";			
				return render_template('landingPage.html', msg=msg);
		else:
			# If the file uploaded is not a txt file, raise error for user.
			msg["msg"] = "File not uploaded.  file must be in txt format.";
			return render_template('landingPage.html', msg=msg)
	else:
		# If it is GET, simply render the landing page.
		msg["msg"] = "none";
		return render_template('landingPage.html', msg=msg)






# Starting up a flask micro-service. 
if __name__ == "__main__":
	app.run(host='localhost', port=5000, threaded=True, debug=True);



