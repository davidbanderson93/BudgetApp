import sys
import sqlite3
from sqlite3 import Error


class Database(object):
	conn = None
	
	def __init__(self, db_file):
		self.conn = self.create_connection(db_file)
	
	def create_connection(self, db_file):
		try:
			conn = sqlite3.connect(db_file)
		except Error as e:
			print e
		return conn
	
	def close_connection(self):
		self.conn.close()
		
	def execute_sql(self, sql_cmd, arg=()):
		try:
			c = self.conn.cursor()
			if not arg:
				c.execute(sqpl_cmd)
			else:
				c.execute(sql_cmd, arg)
		except Error as e:
			print e
		self.conn.commit()

	