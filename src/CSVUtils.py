import csv
import os
from time import time
from datetime import datetime

def prepCSV(csvPath):
	f = open(csvPath, 'r')
	lines = f.readlines()
	f.close()
	ts = time()
	ts = datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
	srcPath = os.path.dirname(csvPath)
	newPath = os.path.join(srcPath, 'statement_%s.csv' % ts)
	f = open(newPath, 'a')
	for i, line in enumerate(lines):
		if i < 4:	# skip the first 4 lines
			continue
		f.write(line)
	f.close()
	os.remove(csvPath)	# remove original file to make room for next exported statement
	return prepPath

def readCSV(csvPath, dict_output=False):
	content = []
	with open(csvPath) as csvFile:
		if dict_output:							# dict reader outputs a key,value pair for each row
												# based on first row as keys
			reader = csv.DictReader(csvFile)
		else:
			reader = csv.reader(csvFile, delimiter=',')
		for row in reader:
			content.append(row)
	return content
	
def writeCSV(budgetPath, procData):
	with open(budgetPath) as budFile:
		fieldnames = ['Transaction Number','Date','Description',
						'Memo','Amount Debit','Amount Credit',
						'Balance','Check Number','Fees']
		writer = csv.DictWriter(budFile, fieldnames=fieldnames)
		writer.writeheader()
		for row in procData:
			writer.writerow(row)	# must be in the same format as it was read in
									# list of dicts with column names as keys and values
		
		