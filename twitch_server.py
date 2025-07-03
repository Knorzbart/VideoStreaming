from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/')
def index():
    return 'Twitch-like streaming server running.'

@socketio.on('stream_frame')
def handle_stream_frame(data):
    """Broadcast video frames from the streamer to all viewers."""
    emit('new_frame', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000)
