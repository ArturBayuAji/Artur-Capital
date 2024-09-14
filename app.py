import os

from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from functools import wraps

from my_forms import RegisterForm, LoginForm, IndicatorAppearance
from my_database import db, SymbolCategory, Symbol, User
from symbols_helper import pre_populate_forex_symbols

load_dotenv()
secret_key = os.environ['flask_secret_key']
app = Flask(__name__)
app.secret_key = secret_key
app.config["UPLOAD_FOLDER"] = r"static\chart_ss"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)
# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# user loader callback
@login_manager.user_loader
def load_user(user_id: str):
    return db.session.execute(db.select(User).filter_by(id=int(user_id))).scalar()


def logout_user_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return abort(code=403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


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
        try:
            username = form.username.data
            email = form.email.data
            password = generate_password_hash(password=form.password.data, method="scrypt", salt_length=16)
            agree_to_terms_services = form.agree_to_terms_services.data
            agree_to_receive_notifs = form.agree_to_receive_notifs.data

            new_user = User(
                username=username,
                email=email,
                password=password,
                agree_to_terms_services=agree_to_terms_services,
                agree_to_receive_notifs=agree_to_receive_notifs
            )
            db.session.add(new_user)
            db.session.commit()
        except Exception as error:
            print(error)
            return redirect(url_for('register'))
        else:
            login_user(new_user)
            flash(message='Create account successful, you have logged in!')
            return redirect(url_for('home'))
    return render_template(template_name_or_list="register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
@logout_user_only
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            username = form.username.data
            user_data = db.session.execute(db.select(User).filter_by(username=username)).scalar()
            if user_data is None:
                raise Exception("user not found")
            if check_password_hash(pwhash=user_data.password, password=form.password.data) is False:
                raise Exception("wrong password")
        except Exception as e:
            if str(e) == "user not found":
                flash(message='Invalid Username')
            elif str(e) == "wrong password":
                flash(message='Invalid Password')
            else:
                print(e)
        else:
            login_user(user_data)
            flash(message='Login successful!')
            return redirect(url_for('home'))

    return render_template(template_name_or_list="login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(message="Logout successful!")
    return redirect(url_for('home'))


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
    with app.app_context():
        db.create_all()
        pre_populate_forex_symbols()

    app.run(debug=True)
