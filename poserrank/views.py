from flask import render_template, redirect, url_for, request, session, jsonify
from poserrank import app, db
from poserrank.models import User, Group

@app.route('/')
def index():
	return render_template('index.html.j2')

@app.route('/top/')
def top():
	users = User.query.all() # connect to the database and retrieve all posers
	return render_template('top.html.j2', users=users) # render the 'top' template, with posers as a local variable passed into the template

# web browsers initially request this page with GET; after the user has filled
# out the form, the 'sign in' button makes a POST request to the same endpoint,
# this time with the login credentials stored in the request
@app.route('/login/', methods=['GET', 'POST'])
def login():
	if request.method == 'GET': # just serve the login page if it's a GET request
		return render_template('login.html.j2')

	if request.method == 'POST': # authenticate the user if it's a POST request
		query = User.query.filter(User.username == request.form['username']) # query the database for users with the entered username
		if query.count() > 0: # check if any results came up
			user = query.first()
			if user.password == request.form['password']: # if the passwords match, log the user in
				session['user'] = jsonify(user)
				return redirect(url_for('index'))
			else:
				return 'wrong password'

		else:
			return request.form['username'] + ' does not exist'


@app.route('/logout/')
def logout():
	session.clear()
	return redirect(url_for('index'))


@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
	if request.method == 'GET':
		return render_template('newuser.html.j2')

	elif request.method == 'POST':
		newUser = User(username=request.form['username'],
					full_name=request.form['full_name'],
					email=request.form['email'],
					password=request.form['password'])
		db.session.add(newUser)
		db.session.commit()
		return redirect(url_for('index'))


@app.route('/groups/')
def groups():
	if 'user' in session:
		query = Group.query.all()
		return render_template('groups.html.j2', groups=query)
	else:
		return redirect(url_for('index'))


@app.route('/groups/new', methods=['GET', 'POST'])
def new_group():
	if 'user' in session:
		if request.method == 'GET':
			return render_template('newgroup.html.j2')

		elif request.method == 'POST':
			newGroup = Group(name=request.form['name'],
						description=request.form['description'])
			db.session.add(newGroup)
			db.session.commit()
			return redirect(url_for('index'))

	else:
		return redirect(url_for('index'))