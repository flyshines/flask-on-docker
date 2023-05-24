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
app.config.from_object("project.config.Config")

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
        model_path = app.config["MODEL_FOLDER"]
        file.save(os.path.join(path, filename))
        fp = path + '/' + filename
        print(fp)
        model = predict.load_model(model_path)
        # Predict single image
        return predict.classify(model, fp)
# 其他示例
# {'2.jpg': {'sexy': 4.3454722e-05, 'neutral': 0.00026579265, 'porn': 0.0007733492, 'hentai': 0.14751932, 'drawings': 0.85139805}}

# Predict multiple images at once
#predict.classify(model, ['/Users/bedapudi/Desktop/2.jpg', '/Users/bedapudi/Desktop/6.jpg'])
# {'2.jpg': {'sexy': 4.3454795e-05, 'neutral': 0.00026579312, 'porn': 0.0007733498, 'hentai': 0.14751942, 'drawings': 0.8513979}, '6.jpg': {'drawings': 0.004214506, 'hentai': 0.013342537, 'neutral': 0.01834045, 'porn': 0.4431829, 'sexy': 0.5209196}}

# Predict for all images in a directory
#predict.classify(model, '/Users/bedapudi/Desktop/')
#


    # return """
    # <!doctype html>
    # <title>upload new File</title>
    # <form action="" method=post enctype=multipart/form-data>
    #   <p><input type=file name=file><input type=submit value=Upload>
    # </form>
    # """
