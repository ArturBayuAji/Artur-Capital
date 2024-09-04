from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
import os

from my_forms import RegisterForm, LoginForm

load_dotenv()
secret_key = os.environ['flask_secret_key']

app = Flask(__name__)
app.secret_key = secret_key
bootstrap = Bootstrap5(app)


@app.route("/")
def home():
    return render_template(template_name_or_list="index.html")


@app.route("/terms-and-services")
def terms_and_services():
    return render_template(template_name_or_list="term-and-services.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        redirect(location='home')
    return render_template(template_name_or_list="register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()  # re-use the Register Form
    if form.validate_on_submit():
        redirect(location='home')
    return render_template(template_name_or_list="login.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
