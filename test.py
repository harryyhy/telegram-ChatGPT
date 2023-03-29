import redis

redis1 = redis.Redis(host="chatbotchatgpt.redis.cache.windows.net", 
                     password="fMxVXGRWg7Z45RXbrKAbypy2ECgJSbAQ0AzCaCzyPNE=", 
                     port=6380, ssl=True)

redis1.incr(1)
print(redis1.get(1))