FROM mongo:latest

#python version
FROM python:3.9

#create folder
RUN mkdir -p /opt/imf
RUN mkdir -p /opt/imf/data

#Install dependencies
COPY requirements.txt /opt/imf
WORKDIR /opt/imf
RUN pip3 install --no-cache-dir -r requirements.txt

