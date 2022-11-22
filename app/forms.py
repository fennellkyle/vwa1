from wtforms import Form, StringField, PasswordField, validators


class RegistrationForm(Form):
	username     = StringField("Username", [validators.Length(min=4, max=25)])
	email        = StringField("Email Address", [validators.Length(min=6, max=35)])
	password     = PasswordField("New Password", [validators.DataRequired()])


class LoginForm(Form):
	username     = StringField("Username", [validators.Length(min=4, max=25)])
	password     = PasswordField("Password", [validators.DataRequired()])