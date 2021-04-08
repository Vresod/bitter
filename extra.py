import hashlib

class Account:
	def __init__(self,name:str,password:str,id:int):
		self.name = name
		self.passhash = hashlib.sha256(password.encode()).hexdigest()
		self.id = id
	def to_dict(self):
		return {'name':self.name,'id':self.id,'passhash':self.passhash}
	@staticmethod
	def from_dict(account_dict:dict,id:int):
		return Account(name=account_dict['name'],password=account_dict['password'],id=id)