import os

from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
)
from werkzeug.utils import secure_filename
from . nsfw_detector import predict

app = Flask(__name__)

@app.route("/")
def hello_world():
    return jsonify(hello="world")


@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)


@app.route("/image/ai", methods=["GET", "POST"])
def scan_ai():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        path = app.config["STATIC_FOLDER"]
        file.save(os.path.join(path, filename))
        model = predict.load_model('./model/saved_model.h5')

        # Predict single image
        return predict.classify(model, path)

    # return """
    # <!doctype html>
    # <title>upload new File</title>
    # <form action="" method=post enctype=multipart/form-data>
    #   <p><input type=file name=file><input type=submit value=Upload>
    # </form>
    # """
