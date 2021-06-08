from flask import Flask, request, jsonify, abort
from backend import Account, validate_account

app = Flask(__name__)

posts = []
accounts = {"anon":Account("anon","")}

"""
DESIGN:
GET /posts = return all posts
POST /posts = make post, return all posts
"""

@app.route('/posts',methods=['GET','POST'])
def get_post_posts():
	if request.method == 'GET': # return list of bleet
		return jsonify(posts)
	else: # make new bleet
		form = dict(request.form)
		valid = validate_account(accounts,request.authorization)
		if not valid:
			abort(403)
		posts.append({"content":form['content'],"author_id":valid.id})
		return jsonify(posts), 201

@app.route('/',methods=['GET'])
def index():
	with open("index.html","r")as indexhtml: output = indexhtml.read()
	txt_posts = ""
	for post in posts[::-1]:
		poster = get_account(accounts,post['author_id']).to_dict()['name']
		txt_posts += f"<p>{poster}</p>\n<p>{post['content']}</p>\n\n"
	output = output.replace("<!--<<POSTS GO HERE>>-->",txt_posts)
	return output

@app.route('/accounts',methods=['GET','POST'])
def get_post_accounts():
	if request.method == 'GET': # DO NOT RETURN PASSHASH
		accounts_no_passhash = []
		for account in accounts:
			accounts_no_passhash.append(account.to_dict())
		return jsonify(accounts_no_passhash)
	else: # making an account
		form = dict(request.form)
		account = Account.from_dict(form)
		accounts.append(account)
		return account.to_dict(), 201

@app.route('/accounts/<int:id>',methods=['GET'])
def get_account(id):
	return accounts

@app.route('/posts/<int:id>',methods=['GET'])
def get_post(id):
	try:
		return posts[id]
	except IndexError as e:
		abort(404)

# handle http errors

@app.errorhandler(404)
def http404(e):
	return {"message":"404 Not Found","code":404}, 404
@app.errorhandler(403)
def http403(e):
	return {"message":"403 Forbidden","code":403}, 403
@app.errorhandler(401)
def http403(e):
	return {"message":"401 Unauthorized","code":401}, 401
