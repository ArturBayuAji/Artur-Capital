from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, EmailField, SubmitField, RadioField, FileField
from flask_wtf.file import FileRequired, FileAllowed


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    email = EmailField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Confirm')


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
