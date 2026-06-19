import os
from flask import Flask, send_from_directory, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__, static_folder='webos')
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    return send_from_directory('webos', 'index.html')

@socketio.on('input')
def handle_input(data):
    # هنا يتم استقبال الأوامر من المتصفح
    print(f"Received: {data}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=10000)
