import hashlib

class Account:
	def __init__(self,name:str,password:str,id:int):
		self.name = name
		self.__passhash = hashlib.sha256(password.encode()).hexdigest()
		self.id = id
	def to_dict(self,internal = False):
		account_as_dict = {'name':self.name,'id':self.id}
		if internal:
			account_as_dict['passhash'] = self.__passhash
		return account_as_dict
	@staticmethod
	def from_dict(account_dict:dict,id:int):
		return Account(name=account_dict['name'],password=account_dict['password'],id=id)
	

def remove_value_from_dict(dictionary:dict,value):
	"""
	takes a dict and removes a value
	"""
	a = dict(dictionary)
	for val in dictionary:
		if val == value:
			del a[val]
	return a 

def get_account(accounts,id:int):
	for account in accounts:
		if account.id == id:
			return account