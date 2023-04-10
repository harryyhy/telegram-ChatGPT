FROM python:3.7

COPY chatbot.py /
COPY requirements.txt /
COPY openai /openai

RUN pip install pip update
RUN pip install -r requirements.txt

# telegram
# ENV ACCESS_TOKEN ***

# Azure redis
# ENV HOST ***
# ENV PASSWORD ***
# ENV REDISPORT ***

ENTRYPOINT ["python", "/chatbot.py"]