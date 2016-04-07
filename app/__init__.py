from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os.path

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


def create_app():
    db.init_app(app)

    # load all the routes
    from .authentication import authenticationAPI
    app.register_blueprint(authenticationAPI)

    from .student import studentAPI
    app.register_blueprint(studentAPI)

    from .teacher import teacherAPI
    app.register_blueprint(teacherAPI)

    # create db file if it does not exists
    if not os.path.exists(app.config["SQLALCHEMY_DATABASE_URI"]):
            db.create_all()
    if not os.path.exists(app.config['TEST_PATH']):
        os.makedirs(app.config['TEST_PATH'])
    if not os.path.exists(app.config['TEST_RESULT_PATH']):
        os.makedirs(app.config['TEST_RESULT_PATH'])
    app.run()