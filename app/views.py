
from app import app
from flask import Flask, render_template, send_from_directory, \
                    redirect, request, Response, stream_with_context, \
                    make_response, flash, url_for, session
# from flask_socketio import SocketIO, emit
from datetime import datetime, timedelta
import os, sys, json, requests
from .models import db, User

vk_app_id=app.config["VK_APP_ID"]
vk_secret_key=app.config["VK_SECRET_KEY"]

#@app.before_request
#def before_request():
#    session.permanent = True
#    session.permanent_session_lifetime = timedelta(minutes=5)


@app.route("/")
@app.route("/index.html")
def index():
    return render_template('index.tmpl', vk_app_id=vk_app_id)


@app.route('/callback', methods=["GET"])
def callback():
    if not request.args.get('code'):
        return redirect("/", code=302)

    response = requests.get("https://oauth.vk.com/access_token?redirect_uri=https://netmyst.ru/callback", params={
        "client_id": vk_app_id,
        "client_secret": vk_secret_key,
        "code": request.args.get('code'),
        "v": "5.103"
    }).json()

    response = requests.get("https://api.vk.com/method/users.get", params={
        "access_token": response["access_token"],
        "fields": "about,bdate,nickname,screen_name,sex,deactivated",
        "v": "5.103"
    }).json()

    if not response or not response.get("response"):
        return render_template('/', code=302)

    vk_user = response.get("response")[0]

    user_id = vk_user["id"]
    user_firstname = vk_user["first_name"]
    user_lastname = vk_user["last_name"]

    auth_type = User.query.filter_by(
        type="vk",
        user_id=str(vk_user["id"])
        ).one_or_none()

    if not auth_type:
        user = User(
            type='vk',
            user_id=user_id,
            first_name=user_firstname,
            created=datetime.now(),
            last_name=user_lastname
        )
        db.session.add(user)
        db.session.commit()

    session['user_id'] = user_id
    return redirect("/profile", code=302)


@app.route('/profile',  methods = ['GET', 'POST'])
def profile():
    if not session.get('user_id'):
        return redirect("/", code=302)

    user = User.query.filter_by(
            type="vk",
            user_id=session.get('user_id')
         ).one_or_none()

    return render_template('profile.tmpl', first_name=user.first_name, last_name=user.last_name)


@app.route('/logout')
def logout():
    if not session.get('user_id'):
        return redirect("/", code=302)

    session.pop('user_id', None)
    return 'logout'


@app.route('/status')
def status():
    version = "{}.{}".format(sys.version_info.major, sys.version_info.minor)
    message = "Hello World from Flask in a uWSGI Nginx Docker container with Python {} on Alpine (default)".format(version)
    return message


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
