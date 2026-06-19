FROM python:3.9-slim
RUN apt-get update && apt-get install -y git
RUN pip install flask flask-socketio eventlet gunicorn
COPY . .
# استخدام gunicorn للتشغيل الإنتاجي
CMD gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:10000 app:app
