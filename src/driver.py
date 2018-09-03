import sys
import CSVUtils
from DatabaseManager import Database
from DataProcessor import *

if __name__ == '__main__':
	args = sys.argv[1:]
	#prepPath = CSVUtils.prepCSV(args[0])
	statement_data = CSVUtils.readCSV(args[0])
	budget_db = Database('..\databases\Budget.db')
	load_statement_info(budget_db, statement_data)
	#budget_db.close_connection()