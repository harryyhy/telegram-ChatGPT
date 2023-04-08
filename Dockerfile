FROM python

COPY chatbot.py ./
COPY requirements.txt ./
COPY openai ./openai

RUN pip install pip update
RUN pip install -r requirements.txt

# telegram
ENV ACCESS_TOKEN 6272770771:AAErGQoJw6Yuw2HVGMH6Tp_KsTZiLHE8BzY

# Azure redis
ENV HOST chatbot-chatgpt.redis.cache.windows.net
ENV PASSWORD VniyXvnT2pUiqKKA15tObD7Pij8oo1kqOAzCaOFMloU=
ENV REDISPORT 6380

ENTRYPOINT ["python", "/chatbot.py"]