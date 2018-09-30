from flask import render_template, redirect, url_for, request, session, jsonify, Blueprint
from poserrank.shared import db
from poserrank.models import User, Group, Membership
import crypt, hashlib

"""
All of the views defined for this project will return either an html document or a redirect.  Endponits serving json
data should start with /api/
For instance: poserrank.com/api/users/3
"""

views = Blueprint('views', __name__)

@views.route('/')
def index():
	return render_template('index.html.j2')

@views.route('/top/')
def top():
	users = User.query.all() # connect to the database and retrieve all posers
	return render_template('top.html.j2', users=users) # render the 'top' template, with posers as a local variable passed into the template

# web browsers initially request this page with GET; after the user has filled
# out the form, the 'sign in' button makes a POST request to the same endpoint,
# this time with the login credentials stored in the request
@views.route('/login/', methods=['GET', 'POST'])
def login():
	if request.method == 'GET': # just serve the login page if it's a GET request
		return render_template('login.html.j2')

	if request.method == 'POST': # authenticate the user if it's a POST request
		query = User.query.filter(User.username == request.form['username']) # query the database for users with the entered username
		if query.count() > 0: # check if any results came up
			user = query.first()
			if user.hash == hashlib.sha256(str.encode(request.form['password']+user.salty_string)).digest(): # if the passwords match, log the user in
				session['user'] = user.serializeable()
				session['user_id'] = user.id  # sloppy hack -- needs to be fixed later
				return redirect(url_for('views.index'))
			else:
				return 'wrong password'

		else:
			return request.form['username'] + ' does not exist'


@views.route('/logout/')
def logout():
	session.clear()
	return redirect(url_for('views.index'))


@views.route('/users/<int:id>', methods=['GET'])
def get_user(id):
	try:
		user = User.query.filter(User.id == id)[0]
	except IndexError:
		return 'User {} not found'.format(id), 404

	if 'json' in request.args and request.args['json'] == 'true':
		return jsonify(user)
	else:
		return render_template('user.html.j2', user=user)


@views.route('/users/<int:id>', methods=['PATCH'])
def patch_user(id):
	try:
		user = User.query.filter(User.id == id)[0]
	except IndexError:
		return 'User {} not found'.format(id), 404

	host, data = request.data.decode('utf-8').split(':', 1)
	if host == 'subtitle' or host == 'profilPic':
		setattr(user, host, data)
		db.session.commit()
		return 'Message received'
	return 'Host invalid'


@views.route('/users/new', methods=['GET', 'POST'])
def new_user():
	if request.method == 'GET':
		return render_template('newuser.html.j2')

	elif request.method == 'POST':
		salt=crypt.mksalt(crypt.METHOD_SHA512)
		newUser = User(username=request.form['username'],
					full_name=request.form['full_name'],
					email=request.form['email'],
					salty_string=salt,
					hash=hashlib.sha256(str.encode(request.form['password']+salt)).digest())
		db.session.add(newUser)
		db.session.commit()
		return redirect(url_for('views.index'))


