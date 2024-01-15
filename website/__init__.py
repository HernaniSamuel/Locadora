from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
DB_NAME = 'concessionaria.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] ='a349095253ab00afdb54f18e302ff110df4b02b916c62772'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.login_view = 'routes.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    from .routes import routes
    app.register_blueprint(routes, url_prefix="/")

    with app.app_context():
        create_database()

    return app


def create_database():
    if not path.exists('instance/' + DB_NAME):
        db.create_all()
