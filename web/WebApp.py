from flask import Flask, render_template, Response, flash, redirect, request, session, abort, url_for;
from werkzeug.utils import secure_filename;
import sys, os;
import flask;
import json;
from time import gmtime, strftime;

# This is where we save uploaded payroll files
UPLOAD_FOLDER = './UploadFiles/';
# The only file extension we will allow is csv, as indicated by the instructions.
ALLOWED_EXTENSIONS = set(['csv'])



sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', 'python_modules/payroll_modules/')));
# Payroll class contains all relevant functionality for payroll load and reporting.
from PayrollClass import PayrollClass;


# Creating flask app
app = Flask(__name__);
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
	API end-point for uploading payroll csv files.
	POST -> As indicated by the instructions, it takes file input (csv).
	GET  -> This call will return the landing page. 
"""
@app.route("/uploadPayrollFile", methods=['GET','POST'])
def UploadPayrollFile():
	# Create a msg object
	msg = {};
	# Check if the request is POST or GET.
	if(request.method == 'POST'):
		# Check if the file exists in the request
		if 'file' not in request.files:
			# If not, return to landing page with msg, indicating that the use must add a file
			# to the form.
			msg["msg"] = "Please upload a payroll file.";
			return render_template('landingPage.html', msg=msg)

		# Grab the file from the request object
		file = request.files['file']
		# Double check if the file is attached correctly and raise user error, if not.
		if file.filename == '':
			msg["msg"] = "Please upload a payroll file.";
			return render_template('landingPage.html', msg=msg)

		# Check to make sure the file uploaded is csv
		if file and allowed_file(file.filename):
			# Create a file name, based on time/date of file upload.
			filename = "payrollFile_"+strftime("%Y%m%d%H%M%S", gmtime());
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename+".csv"));
			# Instantiate a payroll object, to process the payroll file
			payrollObj = PayrollClass();
			msg = payrollObj.ProcessPayrollFile(filename);
			return render_template('landingPage.html', msg=msg);
		else:
			# If the file uploaded is not a csv file, raise error for user.
			msg["msg"] = "File not uploaded. Payroll file must be in csv format.";
			return render_template('landingPage.html', msg=msg)
	else:
		# If it is GET, simply render the landing page.
		msg["msg"] = "none";
		return render_template('landingPage.html', msg=msg)


"""
	This a API end-point for grabbing payroll report data.
	It uses the PayrollClass.
	Input -> No, input, it is a GET request.
	Output -> JSON format of data.
"""
@app.route("/getpayrollreport", methods=['GET'])
def GetPayrollReport():
	# Instantiate a payroll object
	payrollObj = PayrollClass();
	# Grab results from payroll report.
	payrollReport = payrollObj.GetPayrollReport();
	# Return results to client side.
	return json.dumps(payrollReport);


# Starting up a flask micro-service. 
if __name__ == "__main__":
	app.run(host='localhost', port=5000, threaded=True, debug=True);
