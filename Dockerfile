FROM python:3.7

COPY chatbot.py /
COPY requirements.txt /

RUN pip install pip update
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/chatbot.py"]