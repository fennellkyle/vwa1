import pytest
from main import app


def test_index():
	response = app.test_client().get("/")
	assert response.status_code == 200


def test_search_safe():
	response = app.test_client().get("/search-safe?q=Carbon")
	html = response.data.decode()
	assert response.status_code == 200
	assert "atomic number of 6." in html


def test_register():
	response = app.test_client().get("/register")
	assert response.status_code == 200


def test_search_rXSS_1():
	response_1 = app.test_client().get("/search-rXSS-1?q=Carbon")
	response_2 = app.test_client().get("/search-rXSS-1?q=<script>alert()</script>")
	html_1 = response_1.data.decode()
	html_2 = response_2.data.decode()
	assert response_1.status_code == 200
	assert response_2.status_code == 200
	assert "atomic number of 6." in html_1
	assert "<p><script>alert()</script> is not a valid element.</p>" in html_2


def test_ssti_1():
	response_1 = app.test_client().get("/ssti-1")
	response_2 = app.test_client().get("/{{7*7}}")
	html_1 = response_1.data.decode()
	html_2 = response_2.data.decode()	
	assert response_1.status_code == 200
	assert response_2.status_code == 404
	assert "Visit any endpoint that does not exist." in html_1
	assert "<strong>/49</strong>" in html_2


