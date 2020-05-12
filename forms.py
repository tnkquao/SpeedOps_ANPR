from wtforms import Form, StringField, PasswordField, IntegerField, DateTimeField, FloatField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=5, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid mail'), Length(max=50) ])
    username = StringField('Username', validators=[InputRequired(), Length(min=5, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class OffenceForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    license_plate = StringField('License Plate', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    speed = IntegerField('Speed Captured', validators=[InputRequired()])
    fine = FloatField('Amount Fined', validators=[InputRequired()])


class OffenceSearchForm(FlaskForm):
    choices = [('Name', 'Name'),
               ('License Plate', 'License Plate'),
               ('Location', 'Location')]
    select = SelectField('Search for Offence/Ticket:', choices=choices)
    search = StringField('')
    # consider making page for offences and a separate one for ticket issuements
