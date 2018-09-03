# PoserRank

A revolutionary website that allows users to stay up to date with the leading
posers globally, as well as report acts of posery.

# Software Packages Used

1. Flask - http://flask.pocoo.org/
2. Sqlite - https://www.sqlite.org/
3. SQLAlchemy - https://www.sqlalchemy.org/

# Submodules

This project makes use of git submodules to organize its Bulma dependencies.
Submodules are a means of including repository (Bulma) inside another
repo (PoserRank).  Read more about submodules
[here](https://git-scm.com/book/en/v2/Git-Tools-Submodules).

It is important to note that whenever cloning a repo containing submodules, the
submodules are not immediately retrieved, but rather this must be done manually.
To do this, run the following commands in the base directory:

```
git submodule init
```

```
git submodule update
```

# SQLAlchemy

This project also makes use of SQLAlchemy, a python SQL wrapper and toolkit that makes interfacing with SQL databases much cleaner and easier.  SQLAlchemy can also be used to generate databases from the SQLAlchemy models it detects in a project.  The below instructions are a condensed version of those found [here](http://flask-sqlalchemy.pocoo.org/2.3/quickstart/), so if anything doesn't make sense refer back to the source.  To generate your database, do the following:

1. Go to the inner poserrank directory and create a folder named `db`
2. Navigate to the root directory of your PoserRank repo (the one containing .git) and open the python interactive shell
3. Import the application factory 
```
from poserrank import app_factory
```
3. Create an instance of the app
```
app = app_factory(debug=True)
```
4. Import the db
```
from poserrank.shared import db
```
5. Use the application context to make the database
```
with app.app_context():
    db.create_all()
```

That's it!  You can now populate the database with your favorite sqlite browser, or from the interactive shell.

# Before Installation

Make sure you have sqlite3 and SQLAlchemy (not the python packages, just the regular packages) installed.

# Installation and Use

1. Clone the repository to a local repository of choice.
2. Retrieve the Bulma repo at https://github.com/jgthms/bulma (see above instructions)
3. Run the following pip command to install python dependencies from requirements.txt (alternatively using pip3 if your system uses it to handle python3 packages):
```
pip install -r requirements.txt
```
4. Use SQLAlchemy to generate the development database (see instructions under SQLAlchemy)
5. Run run.py with python.
6. Open the index page on a web browser (localhost:5000 by default).

# Useful Links

* Python Sqlite3 Documentation - https://docs.python.org/3/library/sqlite3.html
* Bulma Documentation - https://bulma.io/documentation/overview/start/
* SQLAlchemy Flask Plugin - http://flask-sqlalchemy.pocoo.org/2.3/
