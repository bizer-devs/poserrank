from flask import Flask
from poserrank.shared import db
from flask_migrate import Migrate
from poserrank.tools import ModelEncoder
from poserrank.api import api
from poserrank.views import views
from poserrank.groups import groups

def app_factory(debug=False):
	app = Flask(__name__)
	if debug:
		app.config.from_pyfile('configs/devconfig.py')
		try:
			app.config.from_pyfile('configs/keys.py')
		except RuntimeError:
			# when in debug mode, we can use some generic key if none is provided
			app.config['SECRET_KEY'] = 'notverysecretkey'

	else:
		app.config.from_pyfile('configs/prodconfig.py')
		try:
			app.config.from_pyfile('configs/keys.py')
		except RuntimeError:
			# in prod, not having a keyfile is unacceptable
			raise RuntimeError('Must have a keys.py config for prod')

	app.json_encoder = ModelEncoder  # swap out the encoder for something that will attempt to call serializable()
	db.init_app(app)
	migrate = Migrate(app, db)

	app.register_blueprint(views, url_prefix='')
	app.register_blueprint(groups, url_prefix='/groups')
	app.register_blueprint(api, url_prefix='/api')


	import poserrank.views

	return app
