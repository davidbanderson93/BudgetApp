import sys
import CSVUtils

if __name__ == '__main__':
	args = sys.argv[1:]
	
	#prepPath = CSVUtils.prepCSV(args[0])
	exportData = CSVUtils.readCSV(args[0])
	for e in exportData:
		print e
	
	
	# some data processing
	
	CSVUtils.writeCSV(procData)