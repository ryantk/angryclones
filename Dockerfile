FROM python:3.5-slim

RUN apt-get update && apt-get install -y build-essential x11vnc xvfb

RUN pip3 install pygame
RUN pip3 install pymunk

COPY . /app

WORKDIR /app

CMD python3 angryclones.py

#192.168.91.145