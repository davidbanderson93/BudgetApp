import os
from time import time
from datetime import datetime

DT_FRMT = '%m/%d/%Y'	# used for converting user input date

# match the memo info to category key words to determine category
def determine_category(spending_entry, categories):
	for row in categories:					# categories is a list of dictionaries
		for cat_key, vendor in row.items():	# loop through dictionary
			vendor_fmt = vendor.lower().replace(' ', '')
			if vendor_fmt == '':	# skip this pair if there is no entry
				continue			# this is a consequence of how DictReader parses csv files

			# below: remove spaces and set to lower to ensure high probability of match
			# category vendors are lower case by default but let's be sure
			memo = spending_entry[3].lower().replace(' ', '')
			if vendor_fmt in memo:
				category = cat_key.lower()
				return category	# return the matching category
	return 'unassigned'			# return no category if a match is not found

# load in csv data from statement into spending db table
def load_statement_data(budget_db, statement_data, profile_id, categories):
	# load data from exported csv into spending and attach profile_id to each entry
	for entry in statement_data:
		category = determine_category(entry, categories)
		field_data = {'transaction_number': entry[0], 'date': entry[1],
						'description': entry[2], 'memo': entry[3],
						'debit': entry[4], 'credit': entry[5],
						'balance': entry[6], 'check_number': entry[7],
						'fees': entry[8], 'profile_id': profile_id,
						'category': category}
		if not budget_db.check_data('spending', 'transaction_number', field_data['transaction_number']):
			budget_db.insert_data('spending', field_data)
		
# date_range: [start_date, end_data]
def calc_category_tots(budget_db, categories, date_range={}):
	catKeys = categories[0].keys()
	
	# Calculate totals by category
	spendingTotals = {}
	for cat in catKeys:
		spendingTotals[cat] = 0.
		rows = budget_db.select_data('spending', 'category', cat, select='debit, date')
		for row in rows:
			rowDate = datetime.strptime(row[1], DT_FRMT)	# get date from the current row in the db
			if date_range:	# test if optional date range is present
				if date_range.keys()[0] == 'range_special':			# only care about the end date
					if rowDate <= date_range['range_special'][1]:	# choose the end date to compare to from the dict list
						spendingTotals[cat] += float(row[0])					
				else:
					if date_range['range'][0] <= rowDate <= date_range['range'][1]:	# standard start end range
						spendingTotals[cat] += float(row[0])
			else:	# if no range, then do a full statement range calculation
				spendingTotals[cat] += float(row[0])
		# Convert to positive since the bank statement reports with negatives
		if spendingTotals[cat] < 0.0:
			spendingTotals[cat] *= -1
	
	# Generate spending report
	ts = time()
	reportTime = datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
	reportDir = os.path.join('..', 'reports', reportTime + '.report')
	f = open(reportDir, 'w')
	for cat, total in spendingTotals.items():
		s = "{}: ${}".format(cat, round(total, 2))
		print s
		f.write(s + '\n')
	f.close()
	