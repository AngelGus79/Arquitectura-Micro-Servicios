from Conexion import Conexion
import sqlite3
import sys
print sys.path

try:
	con = Conexion()
	#statement=('CREATE TABLE IF NOT EXISTS Tweets (id INTEGER, screen_name TEXT, comment TEXT);')
	#insert=('INSERT INTO Tweets Values(1,"Miles","tururu"),(2,4,"tururusadad")')
	select=('Select * from Tweets')
	#delete=('delete from Tweets')
	con.connect()
	#con.execute(statement)
	#con.execute(insert)
	print con.execute(select)
	#con.execute(delete)
	con.close()
except sqlite3.Error as error:
	print 'An error occurred:', error.args[0]
