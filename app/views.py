
from app import app
from flask import Flask, render_template, send_from_directory, \
                    redirect, request, Response, stream_with_context, \
                    make_response, flash, url_for
import os, sys, json, requests
from .models import db, User

vk_app_id=app.config["VK_APP_ID"]
vk_secret_key=app.config["VK_SECRET_KEY"]

@app.route("/")
@app.route("/index.html")
def index():
    return render_template('index.tmpl', vk_app_id=vk_app_id)


@app.route('/callback', methods=["GET"])
def callback():
    response = requests.get("https://oauth.vk.com/access_token?redirect_uri=https://netmyst.ru/callback", params={
        "client_id": vk_app_id,
        "client_secret": vk_secret_key,
        "code": request.args.get('code'),
        "v": "5.103"
    }).json()

    response = requests.get("https://api.vk.com/method/users.get", params={
        "access_token": response["access_token"],
        "fields": "sex,bdate,about,deactivated",
        "v": "5.103"
    }).json()

    if not response or not response.get("response"):
        return render_template('index.tmpl')

    vk_user = response.get("response")[0]

    first_name = vk_user["first_name"]
    last_name = vk_user["last_name"]
#    external_auth = model.external_account.ExternalAccount.query.filter_by(
#            type="vk",
#            external_id=str(vk_user["uid"])
#        ).one_or_none()

    return render_template('callback.tmpl', first_name=first_name, last_name=last_name)


@app.route('/status')
def status():
    version = "{}.{}".format(sys.version_info.major, sys.version_info.minor)
    message = "Hello World from Flask in a uWSGI Nginx Docker container with Python {} on Alpine (default)".format(version)
    return message


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

