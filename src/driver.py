import sys
import CSVUtils
from DatabaseManager import Database
from DataProcessor import *

# create databases if they do not already exist
def initialize_database(budget_db):
	# create profile table
	field_names = {'id': 'integer PRIMARY KEY', 'name': 'text', 'paycheck': 'real'}
	budget_db.create_table('profile', field_names)
	
	# create spending table
	field_names = {'transaction_number': 'integer', 'date': 'text', 'description': 'text', 'memo': 'text',
					'debit': 'real', 'credit': 'real', 'balance': 'real', 'check_number': 'integer',
					'fees': 'real', 'profile_id': 'integer', 'category': 'text'}
	budget_db.create_table('spending', field_names)

	# create goals table
	field_names = {'title': 'text', 'description': 'text', 'cost': 'real', 'achieve_by': 'text',
					'achieved': 'integer', 'profile_id': 'integer'}
	budget_db.create_table('goals', field_names)
	
	# create bills table
	field_names = {'title': 'text', 'description': 'text', 'payment': 'real', 'company': 'text',
					'due_date': 'text', 'profile_id': 'integer'}
	budget_db.create_table('bills', field_names)
	
	# create debts table
	field_names = {'title': 'text', 'description': 'text', 'total_debt': 'real',
					'interest_rate': 'real', 'profile_id': 'integer', 'due_date': 'text',
					'payment': 'real', 'achieve_by': 'text', 'achieved': 'integer'}
	budget_db.create_table('debts', field_names)
	
if __name__ == '__main__':
	args = sys.argv[1:]
	
	#prepPath = CSVUtils.prepCSV(args[0])		# this is for actual exported formats from VWCU
	statement_data = CSVUtils.readCSV(args[0])	# eventually this will be automated to extract from
												# the 'statements' directory
	categories = CSVUtils.readCSV('..\categories\categories.csv', dict_output=True)
	
	budget_db = Database('..\databases\Budget.db')
	
	initialize_database(budget_db)
	load_statement_data(budget_db, statement_data, 1, categories)
	budget_db.close_connection()