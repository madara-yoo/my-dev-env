import os
import pty
import os
import select
import subprocess
from flask import Flask, send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__, static_folder='.hidden_os')
# إعداد SocketIO ليعمل مع Eventlet
socketio = SocketIO(app, async_mode='eventlet')

# مسار مجلد الملفات الثابتة
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
        # مراقبة مخرجات الترمينال
        r, _, _ = select.select([master_fd], [], [])
        if master_fd in r:
            data = os.read(master_fd, 1024)
            socketio.emit('output', data.decode('utf-8', 'ignore'))

# إعداد الجلسة الحقيقية (PTY)
master_fd, slave_fd = pty.openpty()
# تشغيل Bash داخل جلسة تيرمينال حقيقية
subprocess.Popen(['/bin/bash'], stdin=slave_fd, stdout=slave_fd, stderr=slave_fd, preexec_fn=os.setsid)

if __name__ == '__main__':
    # البدء بالخلفية
    socketio.start_background_task(read_and_forward)
    # الحصول على البورت من Render أو استخدام 8080 افتراضياً
    port = int(os.environ.get("PORT", 8080))
    # التشغيل باستخدام eventlet للثبات
    socketio.run(app, host='0.0.0.0', port=port)
