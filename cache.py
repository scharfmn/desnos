import os
import redis


def get_cache():
    '''
        if local usage, start at:
            redis-server /usr/local/etc/redis.conf
    '''
    if os.environ.get("REDIS_URL"):  # Heroku
        cache = redis.from_url(os.environ["REDIS_URL"]) #, charset="utf-8", decode_responses=True
    elif os.environ.get("FLASK_APP"):  # local
        cache = redis.StrictRedis(charset="utf-8", decode_responses=True)
    else:  # Docker (with redis on same server)
        cache = redis.StrictRedis(
            charset="utf-8", decode_responses=True, host="redis", port=6379
        )
    return cache

def flush_cache(cache):
    cache.flushdb()


