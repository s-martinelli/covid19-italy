FROM ubuntu:18.04
COPY . /app
WORKDIR /app
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install python3.6 python3-pip -y
RUN pip3 install requests telegram python-telegram-bot
CMD python3.6 ./covid-italy.py