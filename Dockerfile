FROM python:3.8-slim

ADD . /app
WORKDIR /app

CMD ["python", "main.py", "sample.txt"]
