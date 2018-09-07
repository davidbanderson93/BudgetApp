from datetime import datetime

dt_frmt = '%m-%d-%Y'	# used for converting user input date

class UserInput(object):
	profile_id = ''
	title = ''
	description = ''
	data = {}
	
	def __init__(self):
		self.profile_id  = eval(raw_input('Profile ID: '))
		self.title       = raw_input('Title: ')
		self.description = raw_input('Description: ')
		
	def get_data(self):
		return self.data
	
class Goal(UserInput):
	cost = 0.
	achieve_by = ''
	achieved = 0	# integer boolean
	
	def __init__(self, goals_field_names):
		super(Goal, self).__init__()
		self.cost       = eval(raw_input('Cost: '))
		self.achieve_by = raw_input('Achieve By (m-d-yyyy): ')
		
		goals_field_names['profile_id']  = self.profile_id
		goals_field_names['title']       = self.title
		goals_field_names['description'] = self.description
		goals_field_names['cost']        = self.cost
		goals_field_names['achieve_by']  = str(datetime.strptime(self.achieve_by, dt_frmt).date())
		goals_field_names['achieved']    = self.achieved
		
		self.data = goals_field_names
		
class Bill(UserInput):
	payment = 0.
	company = ''
	due_date = ''

	def __init__(self, bills_field_names):
		super(Bill, self).__init__()
		self.payment  = eval(raw_input('Payment: '))
		self.company  = raw_input('Company: ')
		self.due_date = raw_input('Due Date (every month): ')
		
		bills_field_names['profile_id']  = self.profile_id
		bills_field_names['title']       = self.title
		bills_field_names['description'] = self.description
		bills_field_names['payment']     = self.payment
		bills_field_names['due_date']    = eval(self.due_date)
		
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
		self.payment       = eval(raw_input('Payment: '))
		self.total_debt    = eval(raw_input('Total Debt: '))
		self.interest_rate = eval(raw_input('Interest Rate (%): '))
		self.achieve_by    = raw_input('Achieve By (m-d-yyyy): ')
		self.due_date      = raw_input('Due Date (every month): ')
		
		debts_field_names['profile_id']    = self.profile_id
		debts_field_names['title']         = self.title
		debts_field_names['description']   = self.description
		debts_field_names['payment']       = self.payment
		debts_field_names['achieve_by']    = str(datetime.strptime(self.achieve_by, dt_frmt).date())
		debts_field_names['achieved']      = self.achieved
		debts_field_names['due_date']      = eval(self.due_date)
		debts_field_names['total_debt']    = self.total_debt
		debts_field_names['interest_rate'] = self.interest_rate
		
		self.data = debts_field_names
