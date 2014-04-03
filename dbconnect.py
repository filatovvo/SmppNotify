import MySQLdb
import sys
import os
import subprocess
import time

while ('true'):
	# Open database connection
	db = MySQLdb.connect("localhost","smpp","passwordhere","tsmsd" )
	dbupdate = MySQLdb.connect("localhost","smpp","passwordhere","tsmsd")
	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	cursorupdate = dbupdate.cursor()

	# Prepare SQL query to INSERT a record into the database.
	sql = "SELECT text,number,processed,id FROM outbox \
		   WHERE processed <= '%d'" % (0)

	print(sql)
	try:
		cursor.execute(sql)
		# Fetch all the rows in a list of lists.
		results = cursor.fetchall()
		print results
		for row in results:
			text = row[0]
			phone = row[1]
			processed = row[2]
			id = row[3]
			# Now print fetched result
			print "text=%s,phone=%s,processed=%d" % \
						(text, phone, processed )
			if (phone == 'None'):
				print('phone=None')
				sys.exit()
			else:
				try:
					print('Body SQL Here')
					try:
						subprocess.call(["/opt/python-smpplib-master/sendsms.py","-t",text,"-d",phone])
					except:
						print('Check IPSec Connection JOPA')
					sqlupdate = "UPDATE outbox SET processed=1 where id='%d'" % (id)  			
					print(sqlupdate)
					#cursorupdate = dbupdate.cursor()
					
					cursorupdate.execute(sqlupdate)
					#dbupdate.commit()
				except:
					print('Ls')
					#dbupdate.rollback()
					
				
	except:
	   print "Error: unable to fecth data"


	dbupdate.commit()
	dbupdate.close()
	# disconnect from server
	db.close()
	time.sleep(5)
pass

