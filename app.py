import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='localhost', port=6379)  # Change 'redis' to 'localhost'

def get_hit_count():
    retries = 5 # retry 5 times
    while True:
        try:
            return cache.incr('hits') # adding redis key 'hits' and incrementing it
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)