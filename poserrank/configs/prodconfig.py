import os
from poserrank.shared import BASE_DIR

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db/prod.db')