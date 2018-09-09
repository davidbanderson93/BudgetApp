#!/usr/bin/env python
import sys
import CSVUtils
from UserInterface import *
from DatabaseManager import Database
from DataProcessor import *

# create databases if they do not already exist
def initialize_database(budget_db):
	# create profile table
	profiles_field_names = {'id': 'integer PRIMARY KEY', 'first_name': 'text', 'last_name': 'text', 'paycheck': 'real', 'nickname': 'text'}
	budget_db.create_table('profiles', profiles_field_names)
	
	# create spending table
	spending_field_names = {'transaction_number': 'integer', 'date': 'text', 'description': 'text', 'memo': 'text',
					'debit': 'real', 'credit': 'real', 'balance': 'real', 'check_number': 'integer',
					'fees': 'real', 'profile_id': 'integer', 'category': 'text'}
	budget_db.create_table('spending', spending_field_names)

	# create goals table
	goals_field_names = {'title': 'text', 'description': 'text', 'cost': 'real', 'achieve_by': 'text',
					'achieved': 'integer', 'profile_id': 'integer'}
	budget_db.create_table('goals', goals_field_names)
	
	# create bills table
	bills_field_names = {'title': 'text', 'description': 'text', 'payment': 'real', 'company': 'text',
					'due_date': 'integer', 'profile_id': 'integer'}
	budget_db.create_table('bills', bills_field_names)
	
	# create debts table
	debts_field_names = {'title': 'text', 'description': 'text', 'total_debt': 'real',
					'interest_rate': 'real', 'profile_id': 'integer', 'due_date': 'integer',
					'payment': 'real', 'achieve_by': 'text', 'achieved': 'integer'}
	budget_db.create_table('debts', debts_field_names)
	return [goals_field_names, bills_field_names, debts_field_names, profiles_field_names]
	
# cleans up the sql specific types for use in the UserInterface
def clean_field_names(field_names):
	clean_field_names = []
	for table_fields in field_names:			# loop through the list of dicts
		clean_dict = {}
		for key in table_fields.keys():		# loop through key, value sets
			clean_dict[key] = ''			# reset value
		clean_field_names.append(clean_dict)
	return clean_field_names
	
	
# main of the driver
if __name__ == '__main__':
	args = sys.argv[1:]
	
	print "usage: <cmd (new/update)> <table name> <goal/bill/debt title to update>"
	
	#prepPath = CSVUtils.prepCSV(args[0])		# this is for actual exported formats from VWCU
	#statement_data = CSVUtils.readCSV(args[0])	# eventually this will be automated to extract from
												# the 'statements' directory
												
	# load categories from csv file
	categories = CSVUtils.readCSV('..\categories\categories.csv', dict_output=True)
	
	# connect to the budget_db (or create it if does not exist)
	budget_db = Database('..\databases\Budget.db')
	
	field_names = initialize_database(budget_db)		# create tables if do not exist
	cln_field_names = clean_field_names(field_names)	# clean dictionaries but retain keys
	#load_statement_data(budget_db, statement_data, 1, categories)	# load most recent statement data
	
	# look for user input
	if 'new' in args or 'update' in args:
		if   'goal' in args:
			table_name = 'goals'
			data = Goal(cln_field_names[0]).get_data()
		elif 'bill' in args:
			table_name = 'bills'
			data = Bill(cln_field_names[1]).get_data()
		elif 'debt' in args:
			table_name = 'debts'
			data = Debt(cln_field_names[2]).get_data()
		elif 'profile' in args:
			table_name = 'profiles'
			data = Profile(cln_field_names[3]).get_data()
			
		if 'new' in args:
			budget_db.insert_data(table_name, data)
		elif 'update' in args:
			budget_db.update_data(table_name, data, 'title', args[2])	# arg[2] is the title field of desired data
	
	budget_db.close_connection()