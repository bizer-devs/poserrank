from flask import render_template, redirect, url_for, request, session, jsonify
from poserrank import app, db
from poserrank.models import User, Group, Membership

"""
All of the views defined for this project will return either an html document or a redirect.  Endponits serving json
data should start with /api/
For instance: poserrank.com/api/users/3
"""

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
				session['user'] = user.serializeable()
				session['user_id'] = user.id  # sloppy hack -- needs to be fixed later
				return redirect(url_for('index'))
			else:
				return 'wrong password'

		else:
			return request.form['username'] + ' does not exist'


@app.route('/logout/')
def logout():
	session.clear()
	return redirect(url_for('index'))


@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
	try:
		user = User.query.filter(User.id == id)[0]
	except IndexError:
		return 'User {} not found'.format(id), 404

	if 'json' in request.args and request.args['json'] == 'true':
		return jsonify(user)
	else:
		return render_template('user.html.j2', user=user)


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
		user = User.query.filter(User.id == session['user_id'])[0]

		if request.method == 'GET':
			return render_template('newgroup.html.j2')

		elif request.method == 'POST':
			group = Group(name=request.form['name'],
						description=request.form['description'])
			first_membership = Membership(user=user,
										  group=group,
										  is_owner=True)
			db.session.add(group)
			db.session.add(first_membership)
			db.session.commit()
			return redirect(url_for('index'))

	else:
		return redirect(url_for('index'))

@app.route('/groups/<int:id>/adduser', methods=['GET', 'POST'])
def add_user_to_group(id):
	if 'user_id' in session:
		user = User.query.filter(User.id == session['user_id'])[0]
		group = Group.query.filter(Group.id == id)[0]
		try:
			membership = Membership.query.filter(Membership.user == user).filter(Membership.group == group)[0]
		except IndexError:
			return 'You are not a member of this group', 403

		if membership.is_owner:
			if request.method == 'GET':
				return render_template('addusertogroup.html.j2', group=group)
			elif request.method == 'POST':
				try:
					new_member = User.query.filter(User.username == request.form['username'])[0]
				except IndexError:
					return 'User {} does not exist'.format(request.form['username']), 400

				if Membership.query.filter(Membership.user == new_member).filter(Membership.group == group).count() > 0:
					return 'User {} is already a member of this group'.format(request.form['username']), 400

				membership = Membership(user=user,
										group=group,
										is_owner=('is_owner' in request.form))
				db.session.add(membership)
				db.session.commit()
				return redirect(url_for('index'))

		else:
			return 'You are not an owner of this group', 403

	else:
		return redirect(url_for('index'))