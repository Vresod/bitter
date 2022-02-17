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

def get_accounts(id=None): # MAKE THIS NOT RETURN THE PASSWORDS, I CANNOT BE ASSED TO DO IT RIGHT NOW -nick
	with open("jsonfiles/accounts.json","r") as accountsraw:
		accounts = json.loads(accountsraw.read())
		if id is None:
			return accounts
		else:
			return accounts[str(id)]

def make_account(name,password):
	with open("jsonfiles/accounts.json","r") as accountsraw:
		accounts = json.loads(accountsraw.read())
		new_account = {'name':name,'pass':password}
		accounts.append(new_account)
	with open("jsonfiles/accounts.json","w") as accountsraw:
		accountsraw.write(json.dumps(accounts))
	return new_account

def get_posts():
	with open("jsonfiles/posts.json","r") as postsraw:
		x = json.loads(postsraw.read())
		posts = x
		return posts

def make_post(content,author_id,comment_on=None):
	with open("jsonfiles/posts.json","r") as postsraw:
		posts = json.loads(postsraw.read())
		new_post = {'content':content,'author_id':author_id,'id':len(posts),'likes':0,'comment_on':comment_on}
		posts.append(new_post)
	with open("jsonfiles/posts.json","w") as postsraw:
		postsraw.write(json.dumps(posts))

	return new_post

def like_post(id):
	with open("jsonfiles/posts.json","r") as postsraw:
		posts = json.loads(postsraw.read())
		liked_post = posts[id]
		liked_post['likes'] += 1
	with open("jsonfiles/posts.json","w") as postsraw:
		postsraw.write(json.dumps(posts))
	
def get_thread(lowest_id):
	with open("jsonfiles/posts.json","r") as postsraw:
		posts = json.loads(postsraw.read())
	
	lowest = posts[lowest_id]
	thread = []
	post = lowest
	while True:
		thread.append(post)
		if post['comment_on'] == None:
			break
		for x in posts:
			for y in posts:
				reply_count = 0
				if y['comment_on'] == x['id']:
					reply_count += 1
			if x['id'] == post['comment_on']:
				post = x
				post['reply_count'] = 0
				post['reply_count'] = reply_count
				break
	thread.pop(0)
	return thread[::-1]
