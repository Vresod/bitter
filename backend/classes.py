import hashlib
import base64
import argon2

valid_chars = set("abcdefghijklmnopqrstuvwxyz-._~") # too lazy to write this out

class InvalidNameError(Exception): pass
class AccountNotFoundError(Exception): pass

class Account(object):
	def __init__(self,id:int,password:str):
		"""
		Makes a new account. `id` is the username of the account.
		"""
		for char in id.lower():
			if char not in valid_chars:
				raise InvalidNameError("Invalid character '{}' in name".format(char))
		self.id = id
		self.token = base64.urlsafe_b64encode(argon2.argon2_hash(password,"password",argon_type=argon2.Argon2Type.Argon2_id))

	def __repr__(self):
		return "<Account id='{}'>".format(self.id)
	def to_dict(self,internal = False):
		return {"id":self.id,"token":self.token} if internal else {"id":self.id}
	@staticmethod
	def from_dict(account_dict:dict):
		return Account(account_dict['id'],account_dict['password'])