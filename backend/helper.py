import base64
from .classes import AccountNotFoundError

def remove_value_from_dict(dictionary:dict,value):
	"""
	takes a dict and removes a value
	"""
	a = dict(dictionary)
	for val in dictionary:
		if val == value:
			del a[val]
	return a 

def validate_account(accounts,token):
	id = base64.b64decode(token).split(":")[0]
	if id.lower() == "anon": return True
	account = get_account(accounts,id)
	return account if token == account.token else False

def get_account(accounts,id):
	"""
	DOES NOT WORK ON PYTHON <= 3.7, DUE TO USE OF WALRUS OPERATOR. SUCKS TO SUCK!
	"""
	if account := accounts.get(id) == None:
		raise AccountNotFoundError("Account '{}' not found.".format(id))
	else:
		return account