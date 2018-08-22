from poserrank import db


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
	offender_id = db.Column(db.ForeignKey('users.id'), nullable=False)
	score_change = db.Column(db.Integer, nullable=False)
	description = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, nullable=False)

