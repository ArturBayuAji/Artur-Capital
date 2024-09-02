from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)


@app.route("/")
def home():
    return render_template(template_name_or_list="index.html")


@app.route("/terms-and-services")
def terms_and_services():
    return render_template(template_name_or_list="term-and-services.html")


if __name__ == "__main__":
    app.run(debug=True)
