FROM python:3.10-slim-buster

WORKDIR /web
COPY . /web

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "server.py"]
