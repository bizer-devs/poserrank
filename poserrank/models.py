from poserrank.shared import db


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32), unique=True)
	full_name = db.Column(db.String(64))
	email = db.Column(db.String(64), unique=True)
	password = db.Column(db.String(64))
	subtitle = db.Column(db.String(64))
	profilPic = db.Column(db.String(64))

	memberships = db.relationship('Membership', back_populates='user')

#	sent_invitations = db.relationship('Invitations')
#	recieved_invitations = db.relationship('Invitations')

	def serializeable(self):
		return {
			'id': self.id,
			'username': self.username,
			'full_name': self.full_name,
			'email': self.email,
		}

	def __repr__(self):
		return '<User %r>' % self.username


class Membership(db.Model):
	__tablename__ = 'memberships'
	user_id = db.Column(db.ForeignKey('users.id'), primary_key=True)
	group_id = db.Column(db.ForeignKey('groups.id'), primary_key=True)
	score = db.Column(db.Integer, default=0)
	is_owner = db.Column(db.Boolean, default=False)

	user = db.relationship('User', foreign_keys=[user_id], back_populates='memberships')
	group = db.relationship('Group', foreign_keys=[group_id], back_populates='memberships')

	def serializeable(self):
		return {
			'id': self.id,
			'user_id': self.user_id,
			'group_id': self.group_id,
			'score': self.score,
		}

	def __repr__(self):
		return '<Membership %r - %r>' % (self.user.username, self.group.name)


class Group(db.Model):
	__tablename__ = 'groups'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	description = db.Column(db.Text)

	memberships = db.relationship('Membership', back_populates='group')

	def serializeable(self):
		return {
			'id': self.id,
			'name': self.name,
			'full_name': self.full_name,
			'email': self.email,
		}

	def __repr__(self):
		return '<Group %r>' % self.name

class Report(db.Model):
	__tablename__ = 'reports'
	id = db.Column(db.Integer, primary_key=True)
	reporter_id = db.Column(db.ForeignKey('users.id'), nullable=False)
	offender_id = db.Column(db.Integer, nullable=False)
	group_id = db.Column(db.Integer)
	score_change = db.Column(db.Integer, nullable=False)
	description = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, nullable=False)

	# offender_id and group_id are a composite foreign key to memberships
	# https://stackoverflow.com/questions/7504753/relations-on-composite-keys-using-sqlalchemy
	__table_args__ = (db.ForeignKeyConstraint([offender_id, group_id],
											  ['memberships.user_id', 'memberships.group_id']),
					  {})

	reporter = db.relationship('User', foreign_keys=[reporter_id])
	membership = db.relationship('Membership', foreign_keys=[offender_id, group_id])

	def serializeable(self):
		return {
			'id': self.id,
			'reporter_id': self.reporter_id,
			'offender_id': self.offender_id,
			'group_id': self.group_id,
			'score_change': self.score_change,
			'description': self.description,
			'timestamp': self.timestamp,
		}

	def __repr__(self):
		return '<Report %d>' % self.id