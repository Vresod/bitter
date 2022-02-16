from flask import Flask, render_template, request, jsonify, abort
from backend import *

app = Flask(__name__)

posts = []
accounts = [{'id':'anon'}]

"""
DESIGN:
GET /posts = return all posts
POST /posts = make post, return all posts
"""

@app.route('/posts',methods=['GET','POST'])
def get_post_posts():
	if request.method == 'GET': # return list of bites
		return str(get_posts())
	else: # make new bite
		form = dict(request.form)
		if request.authorization is None:
			author_id = 0
		else:
			valid = validate_account(request.authorization)
			author_id = valid.id
		return make_post(content=form['content'],author_id=author_id)

@app.route('/',methods=['GET'])
def index():
	return render_template('index.html',posts=get_posts())

@app.route('/accounts',methods=['GET','POST'])
def get_post_accounts():
	if request.method == 'GET': # DO NOT RETURN PASSHASH
		accounts_no_passhash = []
		for account in accounts:
			accounts_no_passhash.append(account.to_dict())
		return jsonify(accounts_no_passhash)
	else: # making an account
		form = dict(request.form)
		return make_account(name=form['name'],password=form['pass'])

@app.route('/accounts/<int:id>',methods=['GET'])
def get_account(id):
	return get_accounts(id)

@app.route('/posts/<int:id>',methods=['GET'])
def get_post(id):
	try:
		posts = get_posts()
		return posts[str(id)]
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
