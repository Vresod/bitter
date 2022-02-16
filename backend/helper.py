import base64
from .classes import AccountNotFoundError
import json

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

def get_account(id):
	with open("jsonfiles/accounts.json","r") as accountsraw:
		accounts = json.loads(accountsraw.read())
		return accounts["id"]

def get_posts():
	with open("jsonfiles/posts.json","r") as postsraw:
		return json.loads(postsraw.read())

def make_post(content,author_id):
	with open("jsonfiles/posts.json","r") as postsraw:
		posts = json.loads(postsraw.read())
		new_post = {'content':content,'author_id':author_id}
		posts.append(new_post)
	with open("jsonfiles/posts.json","w") as postsraw:
		postsraw.write(json.dumps(posts))

	return new_post