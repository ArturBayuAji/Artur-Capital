from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

import os

from my_forms import RegisterForm, LoginForm, IndicatorAppearance

load_dotenv()
secret_key = os.environ['flask_secret_key']

app = Flask(__name__)
app.secret_key = secret_key
app.config["UPLOAD_FOLDER"] = r"static\chart_ss"
bootstrap = Bootstrap5(app)

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


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


@app.route("/new-trade", methods=['GET', 'POST'])
def new_trade():
    form = IndicatorAppearance()
    if form.validate_on_submit():
        # image upload handling
        chart_image_file = form.chart_capture.data
        # sanitize client's filename
        chart_image_file_name = secure_filename(chart_image_file.filename)
        # create path to save the file
        chart_image_save_path = os.path.join(app.config['UPLOAD_FOLDER'], chart_image_file_name)

        # Check if the file already exists and if it does, add a suffix (1), (2), etc.
        if os.path.exists(chart_image_save_path):
            file_name, file_extension = os.path.splitext(chart_image_file_name)
            counter = 1
            while os.path.exists(chart_image_save_path):
                new_file_name = f"{file_name}({counter}){file_extension}"
                chart_image_save_path = os.path.join(app.config['UPLOAD_FOLDER'], new_file_name)
                counter += 1

        # save the file
        # chart_image_file.save(chart_image_save_path)

        # TODO: save the `chart_image_save_path` on database.

        return redirect(url_for('new_trade'))
    return render_template(template_name_or_list="new_trades.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
