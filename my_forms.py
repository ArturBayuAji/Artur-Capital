from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, EmailField, SubmitField


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    email = EmailField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Confirm')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    login = SubmitField('Login')
