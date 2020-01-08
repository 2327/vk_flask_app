from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')
app.secret_key = os.urandom(24)
db.init_app(app)

with app.app_context():
    from . import views
    db.create_all()


