FROM python:3.8

ADD user.py .

RUN pip install sockets

CMD [ "python", "./user.py" ]