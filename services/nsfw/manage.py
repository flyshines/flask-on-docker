from flask.cli import FlaskGroup

from project import app


# cli = FlaskGroup(app)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002)
