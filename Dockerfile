FROM python:latest

WORKDIR /app

COPY requirements.txt /app/
RUN apt update && apt upgrade -y
 
RUN pip3 install -U pip
#RUN pip3 install -U pyrogram tgcrypto
RUN pip install -upgrade setuptools.
RUN pip install ez_setup

RUN pip3 install -r requirements.txt

COPY . /app

#set a default command

CMD python3 bot.py
