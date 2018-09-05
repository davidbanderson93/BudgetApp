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
		budget_db.insert_data('spending', field_data)
