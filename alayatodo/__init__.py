from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='sqlite:////tmp/alayatodo.db',
        SECRET_KEY='development key',
        USERNAME='admin',
        PASSWORD='default',
        SQLALCHEMY_ECHO=True,
    )

    db.init_app(app)

    from alayatodo import models
    from alayatodo import views

    app.register_blueprint(views.bp)

    return app

def init_db():
    db.drop_all()
    db.create_all()
