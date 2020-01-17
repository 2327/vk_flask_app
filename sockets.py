from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room, \
    close_room, rooms, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app, cors_allowed_origins="*")

# def background_thread():
#     """Example of how to send server generated events to clients."""
#     count = 0
#     while True:
#         socketio.sleep(10)
#         count += 1
#         print('1')
#         socketio.emit('my_response',
#                       {'data': 'Server generated event', 'count': count},
#                       namespace='/test')

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
def index():
    return render_template('ping.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

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

@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    print(message['room'], rooms())
    session['receive_count'] = session.get('receive_count', 0) + 1
    print(session['receive_count'])
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})

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
