FROM python:3

ADD webhook.py /
ADD utils.py /
ADD session.py /
ADD question.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

CMD [ "python", "./webhook.py" ]
