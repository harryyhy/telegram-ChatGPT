FROM python

COPY chatbot.py /
COPY requirements.txt /

RUN pip install pip update
RUN pip install -r requirements.txt

# telegram
ENV ACCESS_TOKEN 6272770771:AAErGQoJw6Yuw2HVGMH6Tp_KsTZiLHE8BzY

# Azure redis
ENV HOST chatbotchatgpt.redis.cache.windows.net
ENV PASSWORD fMxVXGRWg7Z45RXbrKAbypy2ECgJSbAQ0AzCaCzyPNE=
ENV REDISPORT 6380

ENTRYPOINT ["python", "/chatbot.py"]