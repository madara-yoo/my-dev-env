from flask import Flask, send_from_directory
from flask_socketio import SocketIO
import pty
import os
import select
import termios
import struct
import fcntl
import subprocess

app = Flask(__name__, static_folder='.hidden_os')
socketio = SocketIO(app)

@app.route('/')
def index():
    return send_from_directory('.hidden_os', 'index.html')

@socketio.on('input')
def handle_input(data):
    # إرسال المدخلات من المتصفح إلى عملية الـ Terminal
    os.write(master_fd, data.encode())

def read_and_forward():
    while True:
        # قراءة المخرجات من الترمينال وإرسالها للمتصفح
        fd_list = [master_fd]
        readable, _, _ = select.select(fd_list, [], [])
        if master_fd in readable:
            data = os.read(master_fd, 1024)
            socketio.emit('output', data.decode('utf-8', 'ignore'))

# إنشاء جلسة PTY حقيقية
master_fd, slave_fd = pty.openpty()
subprocess.Popen(['/bin/bash'], stdin=slave_fd, stdout=slave_fd, stderr=slave_fd, preexec_fn=os.setsid)

if __name__ == '__main__':
    socketio.start_background_task(read_and_forward)
    socketio.run(app, host='0.0.0.0', port=8080)
