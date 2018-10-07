 #!/usr/bin/env python
import sys
from datetime import datetime
import CSVUtils
import UserInterface as ui
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
	
	# load categories from csv file
	categories = CSVUtils.readCSV('..\categories\categories.csv', dict_output=True)
	
	# connect to the budget_db (or create it if does not exist)
	budget_db = Database('..\databases\Budget.db')
	
	field_names = initialize_database(budget_db)		# create tables if do not exist
	cln_field_names = clean_field_names(field_names)	# cleans dictionaries but retain keys
	
	# Get cmd line args
	args = sys.argv[1:]
	
	if 'help' in args:
		print '''
	Command                Description
	---------------------------------------------------------------------
	load                   Add a path to a statement to load into the db
	new                    Creates a new table db entry
	update                 Updates a current db entry
	calc totals            Generates a spending report for all time
	
	
	Usage Examples:
	----------------------------------------------------------------------
	driver.py load ..\statements\<statement_name.csv>
	driver.py new bill "title of bill"
	driver.py update bill "title of bill"
	driver.py calc totals

	'''
		sys.exit()
	
	print "Running..."
	
	if 'load' in args:
		#prepPath = CSVUtils.prepCSV(args[1])		# this is for actual exported formats from VWCU
		prepPath = args[1]	#temporary assignment
		statement_data = CSVUtils.readCSV(prepPath)	# eventually this will be automated to extract from
													# the 'statements' directory
		load_statement_data(budget_db, statement_data, 1, categories)	# load most recent statement data
	
	# handle user input
	if 'new' in args or 'update' in args:
		table_name = ui.get_table_name(args)	# extract table name form input args
		
		if 'profile' not in table_name:
			# shallow check to ensure the user's cmd can be executed without issue
			if 'new' in args:
				if budget_db.check_data(table_name, 'title', args[2]):		# user must specify the 'title' field when creating
																			# a new db entry. Consider finding an alternative 
																			# interface that pulls in a form and checks everything
																			# at one time.
					print "Cannot create new %s, '%s': It already exists." % (args[1], args[2])
					sys.exit()
			elif 'update' in args:
				if not budget_db.check_data(table_name, 'title', args[2], select='title'):
					print "Cannot update %s, '%s': It does not exist." % (args[1], args[2])
					sys.exit()
		
		data = ui.prompt_user(args, cln_field_names)	# prompt user for data
			
		if 'new' in args:
			budget_db.insert_data(table_name, data)
		elif 'update' in args:
			budget_db.update_data(table_name, data, 'title', args[2])	# arg[2] is the title field of desired data
	
	if 'calc' in args and 'totals' in args:
		calc_category_tots(budget_db, categories, date_range=ui.get_date_range())
	
	budget_db.close_connection()