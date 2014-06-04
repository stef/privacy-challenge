from wtforms import Form, BooleanField, TextField, PasswordField, validators

class RegistrationForm(Form):
    name = TextField('Name', [validators.Length(min=4, max=25)])
    country = TextField('Country', [validators.Length(min=4, max=100)])
    address = TextField('Address', [validators.Length(min=6, max=200)])
    company = TextField('Company/Affiliation', [validators.Length(min=6, max=200)])
    dept = TextField('Department', [validators.Length(min=6, max=200)])
    pos = TextField('Position', [validators.Length(min=6, max=200)])
    serno = TextField('Product Serial No', [validators.Length(min=8, max=8)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])

class LoginForm(Form):
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [ validators.Required(), ])
