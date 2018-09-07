import sys
import CSVUtils
from UserInterface import *
from DatabaseManager import Database
from DataProcessor import *

# create databases if they do not already exist
def initialize_database(budget_db):
	# create profile table
	field_names = {'id': 'integer PRIMARY KEY', 'name': 'text', 'paycheck': 'real'}
	budget_db.create_table('profile', field_names)
	
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
	return [goals_field_names, bills_field_names, debts_field_names]
	
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
	if 'new' in args:
		if   'goal' in args:
			table_name = 'goals'
			data = Goal(cln_field_names[0]).get_data()
		elif 'bill' in args:
			table_name = 'bills'
			data = Bill(cln_field_names[1]).get_data()
		elif 'debt' in args:
			table_name = 'debts'
			data = Debt(cln_field_names[2]).get_data()
	budget_db.insert_data(table_name, data)
	budget_db.close_connection()