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
	
	#	sqpl_cmd: string
	#	arg: tuple
	def execute_sql(self, sql_cmd, arg=()):
		try:
			c = self.conn.cursor()
			if not arg:
				c.execute(sql_cmd)
			else:
				c.execute(sql_cmd, arg)
		except Error as e:
			print e
		self.conn.commit()

	#	table_name: string
	#	field_names: {'field_name': 'SQL field_type',...}
	def create_table(self, table_name, field_names):
		field_string = ''
		for name, field_type in field_names.items():
			field_string += name + ' ' + field_type + ','
		field_string = field_string[:-1]	# remove trailing comma
	
		sql_cmd = 'CREATE TABLE IF NOT EXISTS %s (%s);' % (table_name, field_string)
		print sql_cmd
		self.execute_sql(sql_cmd)
	
	#	table_name: string
	#	field_data: {'field_name': 'field_value',...}
	def insert_data(self, table_name, field_data):
		value_data = ()
		field_names = ''
		for name, value in field_data.items():
			field_names += name + ','
			value_data = value_data + (value,)	# add value to existing tuple
		
		place_holders = ''
		for name in enumerate(field_data.keys()):
			place_holders += '?,'
		
		# remove trailing comma
		field_names = field_names[:-1]
		place_holders = place_holders[:-1]

		sql_cmd = 'INSERT INTO %s(%s) VALUES(%s)' % (table_name, field_names, place_holders)
		self.execute_sql(sql_cmd, arg=value_data)

	#	table_name: string
	#	field_data: {'field_name': 'field_value',...}
	# 	profile_id: integer
	def update_data(self, table_name, field_data, profile_id):
		value_data = ''
		for name, value in field_data.items():
			value_data += name + '=' + '?,'
		value_data = value_data[:-1]
	
		sql_cmd = 'UPDATE %s SET %s WHERE profile_id = %d' % (table_name, value_data, profile_id)
		self.execute_sql(sql_cmd, arg=value_data)
		
	#	table_name: string
	#	profile_id: integer
	def delete_data(self, table_name, profile_id):
		sql_cmd = 'DELETE FROM %s WHERE profile_id=%d' % (table_name, profile_id)
		self.execute_sql(sql_cmd)
		