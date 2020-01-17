from flask import Flask
#from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')
#app.secret_key = os.urandom(24)
app.secret_key = app.config["SECRET_KEY"]

db = SQLAlchemy()
db.init_app(app)
#sess = Session()
#sess.init_app(app)

with app.app_context():
    from . import views

    db.create_all()
