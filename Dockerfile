FROM python:3.9


WORKDIR /usr/src/todolist

ADD . /usr/src/todolist

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "run.py"]