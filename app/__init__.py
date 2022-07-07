from flask import Flask
from config import Config
# from app.models import User, Category
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
import logging

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata=MetaData(naming_convention=naming_convention)
db = SQLAlchemy(metadata=metadata)

migrate = Migrate()
mail = Mail()

login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.login_message = 'Please log in to access this page'

# login_manager = LoginManager()
# login_manager.login_view = 'user.login'
# login_manager.login_message = "Please login to access"

def create_app(config=Config):

    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)

    from app.user import bp as user_bp
    app.register_blueprint(user_bp) 

    from app.base import bp as base_bp
    app.register_blueprint(base_bp)

    from app.dashboard import bp as dash_bp
    app.register_blueprint(dash_bp)

    from app.barang import bp as barang_bp
    app.register_blueprint(barang_bp)

    from app.vendor import bp as vendor_bp
    app.register_blueprint(vendor_bp)

    from app.penjualan import bp as penjualan_bp
    app.register_blueprint(penjualan_bp)

    from app.unit import bp as unit_bp
    app.register_blueprint(unit_bp)

    return app