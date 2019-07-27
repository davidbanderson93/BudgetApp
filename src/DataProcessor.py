import os
from time import time
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

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
			memo = spending_entry[7].lower().replace(' ', '')
			if vendor_fmt in memo:
				category = cat_key.lower()
				return category	# return the matching category
	return 'unassigned'			# return no category if a match is not found

# load in csv data from statement into spending db table
def load_statement_data(budget_db, statement_data, profile_id, categories):
	# load data from exported csv into spending and attach profile_id to each entry
	for entry in statement_data:
		category = determine_category(entry, categories)
		field_data = {'transaction_number': entry[6], 'date': entry[2],
						'description': entry[7], 'memo': entry[7],
						'debit': entry[4], 'credit': entry[4],
						'balance': entry[10], 'check_number': entry[5],
						'fees': entry[4], 'profile_id': profile_id,
						'category': category}
		if not budget_db.check_data('spending', 'transaction_number', field_data['transaction_number']):
			budget_db.insert_data('spending', field_data)
		
# date_range: [start_date, end_data]
# output is a defaultdict with value of list of dicts of date, amount entries for that category
def calc_category_tots(budget_db, categories, date_range={}):
	catKeys = categories[0].keys()
	
	# Calculate totals by category
	spendingTotals = defaultdict(list)
	
	#=========================================================================
	#		Implement filter for certain categories to characterize spending
	#=========================================================================
	for cat in catKeys:
		rows = budget_db.select_data('spending', 'category', cat, select='debit, date')
		for row in rows:
			dollarAmount = 0.	# Initialize for next row amount determination
			rowDate = datetime.strptime(row[1], DT_FRMT)	# get date from the current row in the db
			if date_range:	# test if optional date range is present
				if date_range.keys()[0] == 'range_special':			# only care about the end date
					if rowDate <= date_range['range_special'][1]:	# choose the end date to compare to from the dict list
						dollarAmount = float(row[0])					
				else:
					if date_range['range'][0] <= rowDate <= date_range['range'][1]:	# standard start end range
						dollarAmount = float(row[0])
			else:	# if no range, then do a full statement range calculation
				dollarAmount = float(row[0])
			#if dollarAmount < 0.0:	# Convert to positive since the bank statement reports with negatives
			dollarAmount *= -1	# Changed to multiply by -1 all the time since we want to negate account credits
				
			spendingTotals[cat].append({'date': rowDate, 'amount': dollarAmount})
	return spendingTotals
	
def generate_spending_report(spendingTotals):
	# Generate spending report
	ts = time()
	reportTime = datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
	reportDir = os.path.join('..', 'reports', 'report_%s' % reportTime)
	if not os.path.isdir(reportDir):
		os.mkdir(reportDir)
	graphsDir = os.path.join(reportDir, 'graphs')
	if not os.path.isdir(graphsDir):
		os.mkdir(graphsDir)
	for cat, data in sorted(spendingTotals.items()):
		print "Cat: " + cat + " |", 
		filename = os.path.join(graphsDir, cat.replace(' ', '_') + '.pdf')
		dates = []
		amounts = []
		for entry in data:
			dates.append(entry['date'])
			amounts.append(entry['amount'])
		print "Amount: " + str(sum(amounts))
		plt.plot(dates, amounts)
		plt.savefig(filename)
		
	


	