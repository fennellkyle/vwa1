from flask import render_template, render_template_string, request, session

from main import app, db
from models import Elements


@app.route("/search-rXSS-1")
def search_rxss_1():
	"""
	The use of `|safe` filter explicitely marks `arg` as safe HTML. This should not be used with untrusted input.
	Disabling Jinja autoescaping using the `autoescape false` template would do the same.
	See https://flask.palletsprojects.com/en/latest/templating/#controlling-autoescaping 
	"""
	if request.args.get("q"):
		query = request.args.get("q")
		element = db.session.execute(db.select(Elements).filter_by(name=query)).scalar()
	else:
		query = ""
		element = ""
	return render_template("search-rXSS-1.html", element=element, query=query)


@app.route("/ssti-1")
def ssti_1():
	"""
	Instructions for exploiting the 404 page SSTI vulnerability
	"""
	template = "{% extends 'index.html' %}{% block card %}<article aria-label='Card example'>Visit any endpoint that does not exist. Example: <strong>http://127.0.0.1/thisdoesntexist</strong>. Try and exploit the SSTI vulernability.{% endblock %}"
	return render_template_string(template)


@app.errorhandler(404)
def page_not_found(e):
	"""
	Non-existent pages (404)
	This page has an XXS vulnerability and an SSTI vulernability. The user has control of the template content.
	See https://blog.nvisium.com/p263 
	"""
	main = f"<article align='center'><h2>404</h2>Oops! Sorry that <strong>{request.full_path.strip('?')}</strong> page does not exist.</article>"
	return render_template_string(f"{{% extends 'base.html' %}}{{% block main %}}{main}{{% endblock %}}"), 404