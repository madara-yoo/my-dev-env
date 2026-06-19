FROM python:3.9-slim
# تحديث وتثبيت الأساسيات
RUN apt-get update && apt-get install -y git
RUN pip install flask
# نسخ الملفات
COPY app.py /app.py
COPY .hidden_os /.hidden_os
EXPOSE 8080
# تشغيل السيرفر
CMD ["python3", "/app.py"]
