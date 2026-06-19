FROM python:3.9-slim
RUN apt-get update && apt-get install -y git
# تثبيت مكتبة خفيفة جداً لعمل Terminal في المتصفح
RUN pip install flask
# أنشئ ملف تشغيل بسيط
COPY app.py /app.py
EXPOSE 8080
CMD ["python3", "/app.py"]
