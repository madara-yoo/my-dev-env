FROM python:3.9-slim
RUN apt-get update && apt-get install -y git
RUN pip install flask pexpect
COPY app.py /app.py
COPY .hidden_os /.hidden_os
EXPOSE 8080
CMD ["python3", "/app.py"]
