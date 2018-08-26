from flask import render_template, redirect, url_for, request, session, jsonify, Blueprint
from poserrank.shared import db
from poserrank.models import User, Group, Membership, Report
from datetime import datetime

groups = Blueprint('groups', __name__)


def authenticate(user, group):
	"""
	Tests if user is a member of group
	:param user: either User object or user_id
	:param group: eitehr Group object or group_id
	:return: True if user is in group, False otherwise
	"""

	#attempt to query database for id matching user and group if they are not db objects already
	if type(user) is not User:
		user = User.query.filter(User.id == user)[0]
	if type(group) is not Group:
		group = Group.query.filter(Group.id == group)[0]

	return groups.memberships.filter(Membership.user == user).count() > 0

@groups.route('/groups/')
def index():
	if 'user' in session:
		query = Group.query.all()
		return render_template('groups.html.j2', groups=query)
	else:
		return redirect(url_for('views.index'))


@groups.route('/groups/new', methods=['GET', 'POST'])
def new():
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
			return redirect(url_for('views.index'))

	else:
		return redirect(url_for('views.index'))

@groups.route('/groups/<int:id>/adduser', methods=['GET', 'POST'])
def add_user(id):
	if 'user' in session:
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

				membership = Membership(user=new_member,
										group=group,
										is_owner=('is_owner' in request.form))
				db.session.add(membership)
				db.session.commit()
				return redirect(url_for('views.index'))

		else:
			return 'You are not an owner of this group', 403

	else:
		return redirect(url_for('views.index'))


@groups.route('/groups/<int:group_id>/reportuser', methods=['GET', 'POST'])
def report_user(group_id):
	if 'user' in session and authenticate(request.form['user_id'], group_id):
		if request.method == 'GET':
			return render_template('reportuser.html.j2')

		report = Report(reporter_id=request.form['reporter_id'],
						offender_id=request.form['offender_id'],
						score_change=request.form['score_change'],
						description=request.form['description'],
						timestamp=datetime.utcnow())
		db.session.add(report)
		db.session.commit()

	else:
		return 'Authentication failure', 403