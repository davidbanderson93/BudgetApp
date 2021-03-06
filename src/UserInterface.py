from datetime import datetime

DT_FRMT = '%m/%d/%Y'	# used for converting user input date

def get_date_range():
	start_date = raw_input('From Date (m/d/yyyy): ')
	end_date   = raw_input('  To Date (m/d/yyyy): ')
	if start_date == '' and end_date == '':		# no range
		return {}
	elif start_date != '' and end_date == '':	# start to present
		date_range = {'range': [datetime.strptime(start_date, DT_FRMT), datetime.now()]}
		return date_range
	elif start_date == '' and end_date != '':	# beginning of time to end
		date_range = {'range_special': ['', datetime.strptime(end_date, DT_FRMT)]}
		return date_range
	else:										# standard start to end range
		date_range = {'range': [datetime.strptime(start_date, DT_FRMT), datetime.strptime(end_date, DT_FRMT)]}
		
def get_table_name(args):
	table_name = ''
	if   'goal'    in args: table_name = 'goals'
	elif 'bill'    in args: table_name = 'bills'
	elif 'debt'    in args: table_name = 'debts'
	elif 'profile' in args: table_name = 'profiles'
	return table_name

def prompt_user(args, cln_field_names):
	data = {}
	if   'goal'    in args: data = Goal(cln_field_names[0]).get_data()
	elif 'bill'    in args: data = Bill(cln_field_names[1]).get_data()
	elif 'debt'    in args: data = Debt(cln_field_names[2]).get_data()
	elif 'profile' in args: data = Profile(cln_field_names[3]).get_data()
	return data
	
class UserInput(object):
	profile_id = ''
	title = ''
	description = ''
	
	def __init__(self):
		self.data = {}
		self.profile_id  = raw_input('Profile ID: ')
		self.title       = raw_input('Title: ')
		self.description = raw_input('Description: ')
		
	def get_data(self):
		return self.data
	
class Profile:
	id = 0
	first_name = ''
	last_name = ''
	paycheck = 0.
	nickname = ''

	def __init__(self, profiles_field_names):
		self.first_name = raw_input('First Name: ')
		self.last_name = raw_input('Last Name: ')
		self.nickname = raw_input('Nickname: ')
		self.paycheck = raw_input('Paycheck Amount: ')
		
		profiles_field_names['id'] = self.id	# check routine needs to get next available id
		profiles_field_names['first_name'] = self.first_name
		profiles_field_names['last_name'] = self.last_name
		profiles_field_names['nickname'] = self.nickname
		profiles_field_names['paycheck'] = self.paycheck
		
		self.data = profiles_field_names
	
	def get_data(self):
		return self.data
	
class Goal(UserInput):
	cost = 0.
	achieve_by = ''
	achieved = 0	# integer boolean
	
	def __init__(self, goals_field_names):
		super(Goal, self).__init__()
		self.cost       = raw_input('Cost: ')
		self.achieve_by = raw_input('Achieve By (m/d/yyyy): ')
		self.achieved	= raw_input('Achieved (1 or 0): ')
		
		if self.achieve_by != '':
			self.achieve_by = str(datetime.strptime(self.achieve_by, DT_FRMT).date())
		
		goals_field_names['profile_id']  = self.profile_id
		goals_field_names['title']       = self.title
		goals_field_names['description'] = self.description
		goals_field_names['cost']        = self.cost
		goals_field_names['achieve_by']  = self.achieve_by
		goals_field_names['achieved']    = self.achieved
		
		self.data = goals_field_names
		
class Bill(UserInput):
	payment = 0.
	company = ''
	due_date = ''

	def __init__(self, bills_field_names):
		super(Bill, self).__init__()
		self.payment  = raw_input('Payment: ')
		self.company  = raw_input('Company: ')
		self.due_date = raw_input('Due Date (every month): ')
		
		bills_field_names['profile_id']  = self.profile_id
		bills_field_names['title']       = self.title
		bills_field_names['description'] = self.description
		bills_field_names['payment']     = self.payment
		bills_field_names['company']	 = self.company
		bills_field_names['due_date']    = self.due_date
		
		self.data = bills_field_names
		
class Debt(UserInput):
	payment = 0.
	achieve_by = ''
	achieved = 0
	total_debt = 0.
	interest_rate = 0.
	due_date = ''

	def __init__(self, debts_field_names):
		super(Debt, self).__init__()
		self.payment       = raw_input('Payment: ')
		self.total_debt    = raw_input('Total Debt: ')
		self.interest_rate = raw_input('Interest Rate (%): ')
		self.achieve_by    = raw_input('Achieve By (m/d/yyyy): ')
		self.due_date      = raw_input('Due Date (every month): ')
		self.achieved	   = raw_input('Achieved (1 or 0): ')
		
		if self.achieve_by != '':
			self.achieve_by = str(datetime.strptime(self.achieve_by, DT_FRMT).date())
		
		debts_field_names['profile_id']    = self.profile_id
		debts_field_names['title']         = self.title
		debts_field_names['description']   = self.description
		debts_field_names['payment']       = self.payment
		debts_field_names['achieve_by']    = self.achieve_by
		debts_field_names['achieved']      = self.achieved
		debts_field_names['due_date']      = self.due_date
		debts_field_names['total_debt']    = self.total_debt
		debts_field_names['interest_rate'] = self.interest_rate
		
		self.data = debts_field_names