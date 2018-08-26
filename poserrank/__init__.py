from flask import Flask
from poserrank.shared import db
from flask_migrate import Migrate
from poserrank.tools import ModelEncoder
from poserrank.api import api
from poserrank.views import views

def app_factory(debug=False):
	app = Flask(__name__)
	if debug:
		app.config.from_pyfile('devconfig.py')

	else:
		app.config.from_pyfile('prodconfig.py')
	app.json_encoder = ModelEncoder  # swap out the encoder for something that will attempt to call serializable()
	db.init_app(app)
	migrate = Migrate(app, db)

	app.register_blueprint(views, url_prefix='')
	app.register_blueprint(api, url_prefix='/api')


	import poserrank.views

	return app