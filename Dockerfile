FROM python:3.9-slim
RUN apt-get update && apt-get install -y git
RUN pip install fastapi uvicorn ptyprocess
COPY . .
EXPOSE 10000
CMD ["python", "app.py"]
