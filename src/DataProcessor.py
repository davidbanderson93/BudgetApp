SQL_SPENDING = ''' INSERT INTO spending(transaction_number, date, description, memo, debit, credit, balance, check_number, fees)
				   VALUES(?,?,?,?,?,?,?,?,?) '''

def initialize_database(budget_db):
	# create profile table
	field_names = {'id': 'integer PRIMARY KEY', 'name': 'text', 'paycheck': 'real'}
	budget_db.create_table('profile', field_names)
	
	# create spending table
	field_names = {'transaction_number': 'integer', 'date': 'text', 'description': 'text', 'memo': 'text',
					'debit': 'real', 'credit': 'real', 'balance': 'real', 'check_number': 'integer',
					'fees': 'real', 'profile_id': 'integer'}
	budget_db.create_table('spending', field_names)
	
def load_statement_info(budget_db, statement_data, profile_id):
	# load data from exported csv into spending and attach profile_id to each entry
	for entry in statement_data:
		field_data = {'transaction_number': entry[0], 'date': entry[1], 'description': entry[2], 'memo': entry[3],
						'debit': entry[4], 'credit': entry[5], 'balance': entry[6], 'check_number': entry[7],
						'fees': entry[8], 'profile_id': profile_id}
		budget_db.insert_data('spending', field_data)
		