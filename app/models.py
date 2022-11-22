from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Elements(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False, unique=True)
	symbol = db.Column(db.String(5), nullable=False, unique=True)
	atomic_num = db.Column(db.Integer, unique=True)


class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), index=True, unique=True)
	email = db.Column(db.String(150), unique=True, index=True)
	password_hash = db.Column(db.String(150))

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)