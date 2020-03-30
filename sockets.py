from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from flask_cors import CORS, cross_origin

from datetime import datetime

app = Flask(__name__)
CORS(app, origins='*')
# CORS(app, resources={r"/api/*": {"origins": "*"}})
# cors = CORS(app, resources={r"/api/*": {"origins": "localhost:3000/*"}})

socketio = SocketIO(app, cors_allowed_origins="*")
ROOMS = []

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        print(ROOMS, count)
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')

# @app.route('/socket.io')
# def sessions():
#     return render_template('session.html')
#
# def messageReceived(methods=['GET', 'POST']):
#     print('message was received!!!')
#
# @socketio.on('my event')
# def handle_my_custom_event(json, methods=['GET', 'POST']):
#     print('received my event: ' + str(json))
#     socketio.emit('my response', json, callback=messageReceived)



# #
# #
# #
#
# @app.route('/test/orginate')
# def orginate():
#     socketio.emit('server orginated', 'Something happened on the server!')
#     return '<h1>Sent!</h1>'
#
# @socketio.on('username', namespace='/private')
# def receive_username(username):
#     users[username] = request.sid
#     #users.append({username : request.sid})
#     #print(users)
#     print('Username added!')
#
# @socketio.on('private_message', namespace='/private')
# def private_message(payload):
#     recipient_session_id = users[payload['username']]
#     message = payload['message']
#
#     emit('new_private_message', message, room=recipient_session_id)
#
# @socketio.on('custom event')
# def receive_custom_event(message):
#     print('THE CUSTOM MESSAGE IS: {}'.format(message['name']))
#     emit('from flask', {'extension' : 'Flask-SocketIO'}, json=True)
#
# #
# #
# #


@app.route('/test')
@cross_origin()
def index():
    return render_template('ping.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('my_ping', namespace='/test')
def latency():
    message = round(datetime.utcnow().timestamp())
    print(message)
    emit('my_pong', {'data': message})

@socketio.on('my_list', namespace='/test')
def my_list(message):
    print('444: ', message)
    print('555: ', ROOMS)
    emit('rooms_list', {'data': ROOMS})

@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('disconnect_request', namespace='/test')
def test_disconnect():
    print('Client disconnected')

@socketio.on('pongio', namespace='/test')
def pongio(message):
    print('55: ', message)
    emit('pongio1', {'data': 'pongio2'}, callback=callback())

@socketio.on('pongio1', namespace='/test')
def pongio1(message):
    print('56: ', message)
    emit('pingio2', {'data': 'pongio2'})

def callback():
    print('gavno')

@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)


def generate_numbers(message):
    emit('my_response',
         {'data': '{' + message['first_name'] + message['last_name'] + 'number: 999 }'},
         room=message['room'])


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])

    request_count = session.get('receive_count', 0) + 1
    room_name = message['room']
    first_name = message['first_name']
    last_name = message['last_name']
    user_id = message['user_id']
    # "request_count": {request_count}
    print(f'Action {request_count}. Request {message}')

    if str(message['room']) not in ROOMS:
        ROOMS.append(message['room'])
    my_response = f'"room_name": {room_name}, "first_name": {first_name}, "last_name": {last_name}, "user_id": {user_id}'
    my_list(message)
    emit('my_response', {"data": my_response}, callback=generate_numbers(message))
    background_thread()

@socketio.on('my_room_event', namespace='/test')
def send_room_message(message, methods=['GET', 'POST']):
    session['receive_count'] = session.get('receive_count', 0) + 1
    print(session['receive_count'])
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])

@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})

# @socketio.on('close_room', namespace='/test')
# def close(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
#                          'count': session['receive_count']},
#          room=message['room'])
#     close_room(message['room'])





if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8001, debug=True)
