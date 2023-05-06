import os

from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from . pdf.scan import generate_prompt
from . pdf.scanner import load_recommender

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email


@app.route("/")
def hello_world():
    return jsonify(hello="world")


@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)

@app.route("/pdf/scan", methods=["GET", "POST"])
def scan():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        path = app.config["STATIC_FOLDER"]
        print('path=' + path)
        file.save(os.path.join(path, filename))

        return load_recommender(path + '/' + filename)

@app.route("/pdf/ai", methods=["GET", "POST"])
def scan_ai():
    if request.method == "POST":
        file = request.files["file"]
        question = request.files["question"]
        filename = secure_filename(file.filename)
        path = app.config["STATIC_FOLDER"]
        print('path=' + path)
        file.save(os.path.join(path, filename))

        return generate_prompt(question, path + '/' + filename)
    # return """
    # <!doctype html>
    # <title>upload new File</title>
    # <form action="" method=post enctype=multipart/form-data>
    #   <p><input type=file name=file><input type=submit value=Upload>
    # </form>
    # """
