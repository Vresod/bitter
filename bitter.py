from flask import Flask, request
from flask import json
from flask.json import jsonify
app = Flask(__name__)

posts = []

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
		print(request.form)
		posts.append({"content":request.form['content']})
		return jsonify(posts)