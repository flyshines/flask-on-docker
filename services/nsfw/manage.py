from flask.cli import FlaskGroup

from project import app


# cli = FlaskGroup(app)

if __name__ == "__main__":
    # debug=False threaded=False 单线程跑，否则会有内存泄漏问题，还没有好的解决方案
    app.run(host='127.0.0.1', port=5002, debug=False)
