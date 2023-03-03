FROM python:alpine3.17

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app/
COPY config.py /app/

CMD [ "python3", "main.py" ]
