from flask import Flask, request, jsonify, render_template
import json

from flask.wrappers import Request
import extra
import hashlib
app = Flask(__name__)

posts = []
accounts = [extra.Account("anon","",0)]

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
		if 'id' not in form:
			form['id'] = 0
		elif hashlib.sha256(form.get('password').encode()).hexdigest() != extra.get_account(accounts,int(form['id'])).to_dict(internal=True)['passhash']:
			return {"message":"403 Forbidden","code":403}, 403
		posts.append({"content":form['content'],"author_id":form['id']})
		return jsonify(posts), 201

@app.route('/',methods=['GET'])
def index():
	output = ""
	for x in posts:
		output += f"<p>{x['content']}</p>\n"
	print(output)
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
		account = extra.Account.from_dict(form,len(accounts))
		accounts.append(account)
		return account.to_dict(), 201

@app.route('/accounts/<int:id>')
def get_account(id):
	return extra.get_account(accounts,int(id)).to_dict()

@app.errorhandler(404)
def http404(e):
	return {"message":"404 Not Found","code":404}, 404
