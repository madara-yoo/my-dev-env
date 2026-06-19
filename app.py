import os
import pty
import select
import subprocess
import eventlet
import eventlet.wsgi
from flask import Flask, send_from_directory
from flask_socketio import SocketIO

# إعداد التطبيق
app = Flask(__name__, static_folder='.hidden_os')
socketio = SocketIO(app, async_mode='eventlet')

# مسار الصفحة الرئيسية
@app.route('/')
def index():
    return send_from_directory('.hidden_os', 'index.html')

# التعامل مع مدخلات الترمينال
@socketio.on('input')
def handle_input(data):
    if master_fd:
        os.write(master_fd, data.encode())

def read_and_forward():
    while True:
        r, _, _ = select.select([master_fd], [], [])
        if master_fd in r:
            data = os.read(master_fd, 1024)
            socketio.emit('output', data.decode('utf-8', 'ignore'))

# إعداد الجلسة الحقيقية (PTY)
master_fd, slave_fd = pty.openpty()
subprocess.Popen(['/bin/bash'], stdin=slave_fd, stdout=slave_fd, stderr=slave_fd, preexec_fn=os.setsid)

if __name__ == '__main__':
    # الحصول على البورت من متغير بيئة Render
    port = int(os.environ.get("PORT", 8080))
    
    # تشغيل مهمة القراءة في الخلفية
    eventlet.spawn(read_and_forward)
    
    # تشغيل السيرفر باستخدام eventlet.wsgi (الأكثر استقراراً على Render)
    print(f"Starting server on port {port}...")
    sock = eventlet.listen(('0.0.0.0', port))
    eventlet.wsgi.server(sock, socketio.server)
