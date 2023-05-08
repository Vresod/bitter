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

@app.route('/api/posts',methods=['GET','POST'])
def get_post_posts():
	if request.method == 'GET': # return list of bites
		return # make login function
	else: # make new bite
		print(request.authorization)
		form = dict(request.form)

		if request.authorization is None:
			author_id = 0
		else:
			valid = validate_account(request.authorization)
			author_id = valid['id']

		try:
			comment_on = form['comment_on']
		except KeyError:
			comment_on = None

		return make_post(content=form['content'],author_id=author_id,comment_on=comment_on)

@app.route('/api/posts/<int:id>',methods=['POST'])
def post_comment(id):
	form = dict(request.form)

	if request.authorization is None:
		author_id = 0
	else:
		valid = validate_account(request.authorization)
		author_id = valid.id

	return make_post(content=form['content'],author_id=author_id,comment_on=id)

@app.route('/api/login',methods=['POST'])
def get_post_login():
	form = dict(request.form)

@app.route('/',methods=['GET'])
def index():
	posts = get_posts()
	for x in posts:
		reply_count = 0
		for y in posts:
			if x['id'] == y['comment_on']:
				reply_count += 1
		x['reply_count'] = 0
		x['reply_count'] = reply_count
		posts[x['id']] = x
	return render_template('index.html',posts=posts[::-1],users=get_accounts())

@app.route('/api/accounts',methods=['GET','POST'])
def get_post_accounts(): # making account: {'name':name.'pass':password}
	if request.method == 'GET': # DO NOT RETURN PASSHASH
		accounts_no_passhash = []
		for account in accounts:
			accounts_no_passhash.append({'name':account['name']})
		return jsonify(accounts_no_passhash)
	else: # making an account
		form = dict(request.form)
		return make_account(name=form['name'],password=form['password'])

@app.route('/api/likepost/<int:id>',methods=['post'])
def post_like(id):
	like_post(id)
	post = get_posts()
	post = post[id]
	return post

@app.route('/api/accounts/<int:id>',methods=['GET'])
def get_account(id):
	return get_accounts(id)

@app.route('/posts/<int:id>',methods=['GET'])
def get_post(id):
	try:
		posts = get_posts()
		post = posts[id]
		post['id'] = id

		comments = []
		for x in posts:
			reply_count = 0
			for y in posts:
				if y['comment_on'] == x['id']:
					reply_count += 1
			x['reply_count'] = 0
			x['reply_count'] = reply_count
			if x['comment_on'] == id:
				comments.append(x)

		return render_template("focusedpost.html",post=post,users=get_accounts(),comments=comments,thread=get_thread(lowest_id=id))
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
