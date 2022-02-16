import base64
from .classes import AccountNotFoundError
import json
import argon2

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
	account = get_accounts(id)
	return account if token == account.token else False

def get_accounts(id=None):
	with open("jsonfiles/accounts.json","r") as accountsraw:
		accounts = json.loads(accountsraw.read())
		if id is None:
			return accounts
		else:
			return accounts[str(id)]

def make_account(name,password):
	with open("jsonfiles/accounts.json","r") as accountsraw:
		accounts = json.loadins(accountsraw.read())
		new_account = {'name':name,'pass':password}
		accounts.append(new_account)
	with open("jsonfiles/accounts.json","w") as accountsraw:
		accountsraw.write(json.dumps(accounts))

def get_posts():
	with open("jsonfiles/posts.json","r") as postsraw:
		x = json.loads(postsraw.read())
		posts = x[::-1]
		return posts

def make_post(content,author_id):
	with open("jsonfiles/posts.json","r") as postsraw:
		posts = json.loads(postsraw.read())
		new_post = {'content':content,'author_id':author_id}
		posts.append(new_post)
	with open("jsonfiles/posts.json","w") as postsraw:
		postsraw.write(json.dumps(posts))

	return new_post