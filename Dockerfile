FROM python:latest

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY bot db startup main.py .
COPY config.py .

CMD [ "python3", '-m', "main" ]
