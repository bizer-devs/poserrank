from poserrank import app_factory
from poserrank.shared import db

app = app_factory(debug=True)
with app.app_context():
  db.create_all()