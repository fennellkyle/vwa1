from flask import render_template, request

from main import app, db
from models import Elements


@app.route("/")
def index():
	"""
	Default intro page to the application
	"""
	return render_template("index.html")


@app.route("/search-safe")
def search_safe():
	"""
	Elements Search
	This is a safe implementation
	"""
	if request.args.get("q"):
		query = request.args.get("q")
		element = db.session.execute(db.select(Elements).filter_by(name=query)).scalar()
	else:
		query = ""
		element = ""
	return render_template("search-safe.html", element=element, query=query)