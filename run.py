from poserrank import app_factory

if __name__ == '__main__':
	app = app_factory(debug=True)
	app.run()
