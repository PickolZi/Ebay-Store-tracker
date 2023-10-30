from flask import Flask
from .routes import main
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////instance/db.sqlite3'
    db = SQLAlchemy(app)

    app.register_blueprint(main)

    return db, app