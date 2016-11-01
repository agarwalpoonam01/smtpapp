import smtpd
import datetime
import time
import os
from email.parser import Parser
import email
import sqlite3 as lite

class CustomSMTPServer(smtpd.SMTPServer):
    global peer_g
    global mailfrom_g
    global rcpttos_g
    global data_g
    global date
    global db_name
    global table_name

    
    def initialize_arg(self,db_name_var, table_name_var):
	global db_name 
        global table_name
	db_name = db_name_var
        table_name = table_name_var	
	print "initialized"


    def process_message(self, peer, mailfrom, rcpttos, data):
        global peer_g
        global mailfrom_g
        global rcpttos_g
        global data_g
	global date
	global db_name
	global table_name
        peer_g = peer
        mailfrom_g = mailfrom
        rcpttos_g = rcpttos
        data_g = data
	emaildata =''
	ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print 'Receiving message from:', peer
        print 'Message addressed from:', mailfrom
        print 'Message addressed to  :', rcpttos
        print 'Message length        :', len(data)
	headers = Parser().parsestr(data)
        sub = headers['Subject']
#	body = headers['body']
	emaildata = email.message_from_string(data)
#	print body
	body = emaildata.get_payload()
        rcp = ''
	mail = str(mailfrom)
	db = lite.connect("SMTPSERVER.db")
	cursor = db.cursor()
	for i in range(0,len(rcpttos)):
		sql = """INSERT INTO %s (peer, mailfrom, rcpttos, sub, CONTENT) VALUES('%s','%s', '%s', '%s', '%s')""" %( str(table_name),'localhost', str(mail), str(rcpttos[i]), str(sub), str(body))
		print sql
		try:
	            # Execute the SQL command
		    cursor.execute(sql)
        	    # Commit your changes in the database
	            db.commit()
		    print "Inserted into the db"
		except Exception, msg:
        	    # Rollback in case there is any error
		    print msg
		    print "Unable to insert into db"
	            db.rollback()

        # disconnect from server
        db.close()
        return

