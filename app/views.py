
from app import app
from flask import   Flask, render_template, send_from_directory, \
                    redirect, request, Response, stream_with_context, \
                    make_response, flash, url_for, send_from_directory
import os,sys 

@app.route("/")
@app.route("/index.html")
def index():
    return render_template('index.tmpl')


@app.route('/callback', methods=["GET"])
def callback():
#    user_id = request.args.get('user_id')
#    access_token = request.args.get('access_token')
#    expires_in = request.args.get('expires_in')
    return render_template('callback.tmpl')


#@app.route('/<path:path>')
#def static_file(path):
# if request.method == 'POST':
#  elif request.method == 'GET':
#    return app.send_static_file(path)


@app.route('/status')
def status():
    version = "{}.{}".format(sys.version_info.major, sys.version_info.minor)
    message = "Hello World from Flask in a uWSGI Nginx Docker container with Python {} on Alpine (default)".format(version)
    return message



@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

