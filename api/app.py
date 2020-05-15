import json

from flask import Flask, request, Response
from flask_cors import CORS
import smtplib, ssl
import api
import db

from settings import IS_PRODUCTION

application = Flask(__name__)
CORS(application)


@application.route("/healthstatus", methods=['GET'])
def getHealthStatus():
	"""
	GET healthstatus endpoint. Confirms db connectivity
	as part of health check. Not in api.py because that
	file will not load if db connection is bad

	:return: response object with health status
	"""
	
	try:
		from db import Session
		status=200
		message="Healthy"
	
	# cant talk to db, unhealthy
	except:
		status=400
		message="Unhealthy"

	return(Response(response=json.dumps({"db_status": message}), status=status, mimetype='application/json'))


@application.route("/rawTextEntry", methods=['POST'])
@api.requires_auth
def addRawTextEntry():
	"""
	Adds raw text entry

	:return: response object
	"""
	return api.postRawTextEntry()


@application.route("/processedTextEntry", methods=['POST'])
@api.requires_auth
def addProcessedTextEntry():
	"""
	Adds processed text entry

	:return: response object 
	"""
	return api.postProcessedTextEntry()


@application.route("/rawTextEntries", methods=['GET'])
@api.requires_auth
def getRawTextEntries():
	"""
	Gets raw text entries

	:return: response object with raw text entries 
	"""
	return api.getRawText()


@application.route("/instantProcessing", methods=['POST'])
@api.requires_auth
def instantProcessing():
	"""
	Instant proccessing for raw entries

	:return: response object with proccessed text entry
	"""
	return api.instantProcessing()


@application.route("/processedTextEntries", methods=['GET'])
@api.requires_auth
def getProcessedTextEntries():
	"""
	Returns processed entries

	:return: response object with processed entry list
	"""
	return api.getProcessedText()


@application.route("/deleteProcessedTextEntry", methods=['DELETE'])
@api.requires_auth
def deleteProcessedTextEntry():
	"""
	Deletes processed entry

	:return: response object 
	"""
	return api.deleteProcessedText()


@application.route("/deleteRawTextEntry", methods=['DELETE'])
@api.requires_auth
def deleteRawTextEntry():
	"""
	Deletes raw entry

	:return: response object 
	"""
	return api.deleteRawText()


@application.route("/sources", methods=['GET'])
@api.requires_auth
def getSources():
	"""
	Returns valid sources

	:return: response object with valid sources
	"""
	return api.getSources()


@application.route("/login", methods=['POST'])
def login():
	"""
	Returns a JWT on successful login attempt

	:return: response object with JWT
	"""
	return api.login()

@application.route("/logout", methods=['POST'])
def logout():
	"""
	Deletes user's session key

	:return: response object with JWT
	"""
	return api.logout()


@application.route("/createAccount", methods=['POST'])
def createAccount():
	"""
	Creates a new user account

	:return: response object 
	"""
	return api.createAccount()


@application.route("/email", methods=['POST'])
@api.requires_auth
def email():
	"""
	Creates email alert

	:return: response object 
	"""
	return api.email()


@application.route("/csv", methods=['POST'])
@api.requires_auth
def uploadCSV():
	"""
	Upload CSV

	:return: response object 
	"""
	return api.upload_csv()

# runs app
if __name__ == '__main__':
	if (IS_PRODUCTION):
		application.run(host="0.0.0.0")
	else:
		application.run(debug=True)
