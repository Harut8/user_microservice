import redis


class RedisClient:

    def __init__(self):
        self._connection = redis.Redis(
            host='localhost',
            port=6379)
        print('REDIS CONNECTED')

    @classmethod
    def set_var(cls, key, value, time):
        cls()._connection.set(key, value, time)
        return True

    @classmethod
    def get_var(cls, key):
        return cls()._connection.get(key)
