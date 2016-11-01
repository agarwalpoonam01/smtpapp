from app import app
import smtpd
import asyncore
import smtplib
import email.utils
from email.mime.text import MIMEText
from server import CustomSMTPServer
import threading
from flask import Flask, make_response, request, jsonify
import json
import datetime
import os
import logging
import sys
import sqlite3 as lite

global peer_g
global mailfrom_G
global rcpttos_g
global data_g
global sub_g
global date_time_g
global db_name
global table_name
global OUTPUT_DIRECTORY
OUTPUT_DIRECTORY  = "/var/log/smtpserver/"
peer_g = ''
mailfrom_g = ''
rcpttos_g = ''
data_g = ''
db_name = 'SMTPSERVER'
table_name = 'EMAIL'
sub_g = ''
date_time_g = ''

#Initiallizing log directory
@app.route('/initialize/', methods=["POST"])
def intiallize():
        Response = {}
        Response["Status"] = "Stdout is  initiallized"
        logger = logging.getLogger()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger.setLevel(logging.DEBUG)
	global OUTPUT_DIRECTORY
        if request.headers['Content-Type'] == 'application/json':
                data = request.json
                if not data["log_filename"] == "":

                        filename = OUTPUT_DIRECTORY+data["log_filename"]
                        print filename
			file1 = open(filename,'w+')
                        fh = logging.FileHandler(filename)
                        fh.setFormatter(formatter)
                        logger.addHandler(fh)
                        Response = {}
                        Response["STATUS"] = "Log initiallized"
                        Response["filename"] = filename
                        status = "STATUS", Response
                        logging.info( status )
                        response = make_response(json.dumps(Response, sort_keys=True, indent=4))
                        return response
                else:
                        ch = logging.StreamHandler(sys.stdout)
                        ch.setFormatter(formatter)
                        logger.addHandler(ch)
                        status = "STATUS", Response
                        logging.info(status)
        response = make_response(json.dumps(Response, sort_keys=True, indent=4))
        return response

#Creating database and table should be a one time activity
@app.route('/create_db/', methods=['POST'])
def create_db():
	global db_name
	global table_name
	db = lite.connect('SMTPSERVER.db')
	cursor = db.cursor()
	
	try:
                # Drop table if it already exist using execute() method.
		cursor.execute("DROP TABLE IF EXISTS %s" % str(table_name))
		status = "TABLE DROPPED"
		logging.info( status )
                # Create table as per requirement
		sql = '''CREATE TABLE %s (peer VARCHAR(20), mailfrom VARCHAR(100),rcpttos VARCHAR(100), sub VARCHAR(100), CONTENT TEXT, date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ) ''' % str(table_name)
		cursor.execute(sql)
		status = "TABLE created"
		logging.info( status )
	except Exception, msg:
		print msg
		status = "Failure createing table"
		logging.info( status )
	db.close()
        response = {}
        response["STATUS"] = "DATABASE and TABLE created", db_name, table_name
	response_to_return = make_response(json.dumps(response, sort_keys=True, indent=4))
        return response_to_return

#Gives latest email received by emailid
@app.route('/latest_email_received/<email_id>', methods=["GET"])
def latest_email_received_code(email_id):
    global table_name
    global date_time_g 
    print "hello"
    response = dict()
    status_res="Success"
    result = {}
    db = lite.connect('SMTPSERVER.db')
    cursor = db.cursor()
    sql = "SELECT * FROM %s \
       WHERE rcpttos = '%s' ORDER BY date_time DESC LIMIT 1" % (str(table_name),str(email_id))
    print sql
    try:
        # Execute the SQL command
        cursor.execute(sql)
	status = "Latest email query executed successfully"
	logging.info( status )
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in results:
	        result["peer"] = row[0]
        	result["mailfrom"] = row[1]
	        result["rcpttos"] = row[2]
        	result["sub"] = row[3]
	        result["body"] = row[4]
		result["date_time"] = str(row[5])
        # Now print fetched result
    except Exception, msg:
        print msg
	status = "Failure unable to fecth data"
	logging.info( status )
    # disconnect from server
    db.close()
    f = '%Y-%m-%d %H:%M:%S'
    print result
    response["Status"]=status_res
    response["EMAIL"]=result
    response_to_return = make_response(json.dumps(response, sort_keys=True, indent=4))
    return response_to_return

#Returns all the email id after a particular timestamp
@app.route('/received_since/<date_time>', methods=["GET"])
def received_since(date_time):
    global peer_g
    global mailfrom_g
    global rcpttos_g
    global data_g
    global sub_g
    global date_time_g
    global db_name
    global table_name
    response = dict()
    status_res = "Success"
    count = 0
    response_to_return = ''
    print "hello"
    f = '%Y-%m-%d %H:%M:%S'
    date_t = datetime.datetime.strptime(date_time,f)
    date_t.strftime(f)
    db = lite.connect('SMTPSERVER.db')
    cursor = db.cursor()
    sql = "SELECT * FROM %s \
       WHERE date_time >= '%s' " % (str(table_name),date_t)
    try:
        # Execute the SQL command
        cursor.execute(sql)
	status = "Email since query Executed successfully"
	logging.info( status )
        # Fetch all the rows in a list of lists.
	result = {}
	data = []
        results = cursor.fetchall()
	i = True
        for row in results:
		count+=1
		result["peer"] = row[0]
		result["mailfrom"] = row[1]
		result["rcpttos"] = row[2]
		result["sub"] = row[3]
		result["body"] = row[4]
		result["date_time"] = str(row[5])
		data.append(dict(result))

    except Exception, msg:
        print msg
	status = "Failure unable to fecth data"
	logging.info( status )
    # disconnect from server
    db.close()
    response["Status"]=status_res
    response["Count"]=count
    response["EMAILS"]=data
    response_to_return = make_response(json.dumps(response, sort_keys=True, indent=4))
    return response_to_return


@app.route('/index/', methods=["GET"])
def index():
	return "index code"

def start_server_code():
    global db_name
    global table_name
    server = CustomSMTPServer(('0.0.0.0', 1025), None)
    server.initialize_arg(db_name,table_name)
    asyncore.loop()
    return 'App to get the apis to store get and delete data'

#starts the smtp server
@app.route('/start_server/', methods=["POST"])
def start_server():
    t = threading.Thread(target=start_server_code)
    t.start()
    return 'App to get the apis to store get and delete data'

