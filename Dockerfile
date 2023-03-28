FROM python

COPY chatbot.py /
COPY requirements.txt /

RUN pip install pip update
RUN pip install -r requirements.txt

# # heroku
# ENV ACCESS_TOKEN 6272770771:AAErGQoJw6Yuw2HVGMH6Tp_KsTZiLHE8BzY
# # redis
# ENV HOST redis-10924.c299.asia-northeast1-1.gce.cloud.redislabs.com
# ENV PASSWORD VXmUlR47Ui2uCSRhgtcXhYBjHGL7HRB7
# ENV REDISPORT 10924

ENTRYPOINT ["python", "/chatbot.py"]