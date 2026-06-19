import os
import pty
import select
import subprocess
from flask import Flask, send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__, static_folder='webos')
socketio = SocketIO(app, async_mode='eventlet')

# إعداد الـ Terminal
master_fd, slave_fd = pty.openpty()
subprocess.Popen(['/bin/bash'], stdin=slave_fd, stdout=slave_fd, stderr=slave_fd, preexec_fn=os.setsid)

@app.route('/')
def index():
    return send_from_directory('webos', 'index.html')

@socketio.on('input')
def handle_input(data):
    os.write(master_fd, data.encode())

def read_and_forward():
    while True:
        r, _, _ = select.select([master_fd], [], [])
        if master_fd in r:
            data = os.read(master_fd, 1024)
            socketio.emit('output', data.decode('utf-8', 'ignore'))

if __name__ == '__main__':
    socketio.start_background_task(read_and_forward)
    socketio.run(app, host='0.0.0.0', port=10000)
