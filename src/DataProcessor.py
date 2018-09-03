SQL_SPENDING = ''' INSERT INTO spending(transaction_number, date, description, memo, debit, credit, balance, check_number, fees)
				   VALUES(?,?,?,?,?,?,?,?,?) '''

def load_statement_info(budget_db, statement_data):
	for entry in statement_data:
		spending_entry = (entry[0], entry[1], entry[2], entry[3],
							entry[4], entry[5], entry[6], entry[7], entry[8])
		budget_db.execute_sql(SQL_SPENDING, arg=spending_entry)
		