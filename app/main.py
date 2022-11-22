from flask import Flask
from flask_login import LoginManager

from models import User


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///sqlite.db'
app.config['SECRET_KEY'] = '6rPjvjn5aXakzoldlV7zGcqFTeQcgkSJ'


from models import db
db.init_app(app)
with app.app_context():
	db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	"""
	user_loader callback, which is reponsible for fetching the current user id
	"""
	return User.query.get(user_id)

from views import auth, safe, exercises
