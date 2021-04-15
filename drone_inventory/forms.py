from flask_wtf import FlaskForm
#import fields we need from WTForms
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

#for email, password and submit button
class UserLoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField()