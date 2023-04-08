FROM python

COPY chatbot.py /
COPY requirements.txt /

RUN pip install pip update
RUN pip install -r requirements.txt

# telegram
ENV ACCESS_TOKEN 6272770771:AAErGQoJw6Yuw2HVGMH6Tp_KsTZiLHE8BzY

# Azure redis
ENV HOST chatbot-chatgpt.redis.cache.windows.net
ENV PASSWORD bgmU5bsxVOYLwQ2qF61PVL15ZtsaSFpYZAzCaNUWAQo==
ENV REDISPORT 6380

ENTRYPOINT ["python", "/chatbot.py"]