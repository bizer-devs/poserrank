from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from poserrank.tools import ModelEncoder

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/development.db'
app.json_encoder = ModelEncoder  # swap out the encoder for something that will attempt to call serializable()
db = SQLAlchemy(app)

app.secret_key = 'pushingakeytogithubisterriblepractice'

import poserrank.views
