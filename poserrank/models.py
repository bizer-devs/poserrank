from poserrank import db

# This is an Association Table, which tracks the Many-to-Many relationship
# between Users and Groups.  Many-to-Many refers to the fact that each User can
# belong to many Groups, and that each Group can have many Users.  In the
# in the context of database relationships, 'many' generally means 'more than
# one'

association_table = db.Table('Membership', db.Model.metadata,
	db.Column('user_id', db.Integer, db.ForeignKey('Users.id')),
	db.Column('group_id', db.Integer, db.ForeignKey('Groups.id'))
)

class User(db.Model):
	__tablename__ = 'Users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32), unique=True)
	full_name = db.Column(db.String(64))
	email = db.Column(db.String(64), unique=True)
	password = db.Column(db.String(64))
	score = db.Column(db.Integer, default=0)

	# the User model's means of accessing the 'Membership' relationship; I'm not
	# quite sure how this syntax works, see this link for more info
	# http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#many-to-many
	groups = db.relationship('Group',
		secondary=association_table,
		back_populates='users')

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

class Group(db.Model):
	__tablename__ = 'Groups'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	description = db.Column(db.Text)

	users = db.relationship('User',
		secondary=association_table,
		back_populates='groups')

#	invitations = db.relationship('Invitations')

	def serializeable(self):
		return {
			'id': self.id,
			'name': self.name,
			'full_name': self.full_name,
			'email': self.email,
		}

	def __repr__(self):
		return '<Group %r>' % self.name

"""class Invitation(db.Model):
	__tablename__ = 'Invitations'
	id = db.Column(db.Integer, primary_key=True)
	sender_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
	recipient_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
	group_id = db.Column(db.Integer, db.ForeignKey('Group.id'))"""
