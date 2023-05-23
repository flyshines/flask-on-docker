import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/project/static"
    MODEL_FOLDER = f"{os.getenv('APP_FOLDER')}/project/model/saved_model.h5"
    MEDIA_FOLDER = f"{os.getenv('APP_FOLDER')}/project/media"
