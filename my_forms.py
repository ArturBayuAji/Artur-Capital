from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, EmailField, SubmitField, RadioField, FileField, BooleanField
from flask_wtf.file import FileRequired, FileAllowed


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    email = EmailField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    agree_to_terms_services = BooleanField("I agree to the terms of services.", validators=[validators.DataRequired()])
    agree_to_receive_notifs = BooleanField(
        "I want to be notified of exclusive offers, news product, upcoming betas, and the latest news from "
        "Artur-Capital. (Optional)",
    )
    submit = SubmitField('Create Account')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    login = SubmitField('Login')


class IndicatorAppearance(FlaskForm):
    slow_ma = RadioField("Slow Moving Average", choices=[("Yes", "Yes"), ("No", "No")], validators=[validators.DataRequired()])
    moderate_ma = RadioField("Moderate Moving Average", choices=[("Yes", "Yes"), ("No", "No")], validators=[validators.DataRequired()])
    fast_ma = RadioField("Fast Moving Average", choices=[("Yes", "Yes"), ("No", "No")], validators=[validators.DataRequired()])
    osma = RadioField("OsMA", choices=[("Yes", "Yes"), ("No", "No")], validators=[validators.DataRequired()])
    chart_capture = FileField(
        label='Chart Screen Shoot',
        validators=[
            FileRequired(),
            FileAllowed(upload_set=['jpg', 'png', 'jpeg'], message='only .jpg, .png, .jpeg allowed.')]
    )
    update = SubmitField("Upload")
