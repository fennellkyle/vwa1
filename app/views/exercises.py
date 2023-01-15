import os
import zipfile
from deep_translator import GoogleTranslator, exceptions
from flask import render_template, render_template_string, request, flash, session, abort
from io import BytesIO
from xml.dom.pulldom import parseString
from xml.sax import make_parser
from xml.sax.handler import feature_external_ges


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


@app.route("/search-sqli-1")
def search_sqli_1():
	"""
	Vulnerability: SQL injection
	Untrusted user input is concatenated to a database query. 
	"""
	if request.args.get("q"):
		query = request.args.get("q")
		element = db.session.execute(f'SELECT * FROM elements WHERE name="{query}";').fetchone()
	else:
		query = ""
		element = ""
	return render_template("search-sqli-1.html", element=element, query=query)
 

@app.route("/ssti-1")
def ssti_1():
	"""
	Instructions for exploiting the 404 page SSTI vulnerability
	"""
	template = "{% extends 'index.html' %}{% block card %}<article aria-label='Card example'>Visit any endpoint that does not exist. Example: <strong>http://127.0.0.1/thisdoesntexist</strong>. Try and exploit the SSTI vulernability.{% endblock %}"
	return render_template_string(template)


@app.route("/translate-xxe-1", methods=["GET", "POST"])
def translate_xxe_1():
    """
    The XML parser is configured to process external entities. Newer versions of 'pulldom' disable this by default. See https://docs.python.org/3/library/xml.dom.pulldom.html#module-xml.dom.pulldom
	"""
    read_content = ""
    translated = ""
    if request.method == "POST":
        document = request.files['file']
        file_ext = os.path.splitext(document.filename)[1]
        if document.filename != "" and file_ext in app.config['UPLOAD_EXTENSIONS']:
            if file_ext == ".txt":
                read_content = document.read().decode("utf-8")
            elif file_ext == ".docx":
                docx_zip = zipfile.ZipFile(BytesIO(document.read()))
                docx_file = docx_zip.read('word/document.xml')
                parser = make_parser()
                parser.setFeature(feature_external_ges, True) # Overriding the safe defaults.
                parsed_xml = parseString(docx_file.decode(), parser=parser)
                for event, node in parsed_xml:
                    if event == "CHARACTERS":
                        read_content += f'{node.toxml()}\n'
            try:
                translated = GoogleTranslator(source='auto', target='ja').translate(read_content)
            except exceptions.NotValidLength:
                flash("Text length needs to be between 0 and 5000 char")
                translated = ""
        elif document.filename == "":
            flash("No file selected.")
        elif file_ext not in app.config['UPLOAD_EXTENSIONS']:
            flash("Wrong filetype. Use only txt or docx files")
    return render_template("translate-xxe-1.html", source=read_content, translated=translated)


@app.errorhandler(404)
def page_not_found(e):
	"""
	Non-existent pages (404)
	This page has a SSTI vulernability. The user has control of the template content.
	See https://blog.nvisium.com/p263 
	"""
	bad_chars = set("<>")
	path = request.full_path
	if any((x in bad_chars) for x in path):
		main = f"<article align='center'><h2>404</h2>Nice try! No XSS here.</article>"
	else: 
		main = f"<article align='center'><h2>404</h2>Oops! Sorry that <strong>{request.full_path.strip('?')}</strong> page does not exist.</article>"
	return render_template_string(f"{{% extends 'base.html' %}}{{% block main %}}{main}{{% endblock %}}"), 404