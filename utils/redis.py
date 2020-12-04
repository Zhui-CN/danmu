import redis


class RedisSession:
    _pool = redis.ConnectionPool(host="47.105.131.58", port=6379, db=1)

    @property
    def get_session(self):
        return redis.Redis(connection_pool=self._pool, decode_responses=True)

    @classmethod
    def get_url(cls, name):
        session = cls().get_session
        url = session.rpop(name)
        url = url.decode() if isinstance(url, bytes) else url
        session.lpush(name, url)
        return url

    @classmethod
    def set_url(cls, name, value):
        session = cls().get_session
        session.lpush(name, value)

    @classmethod
    def get_cookie(cls, name):
        session = cls().get_session
        cookie = session.rpop(name)
        cookie = cookie.decode() if isinstance(cookie, bytes) else cookie
        return cookie

    @classmethod
    def set_cookie(cls, name, value):
        if value:
            session = cls().get_session
            session.lpush(name, value)

    @classmethod
    def lrange(cls, name, start, end):
        session = cls().get_session
        data_ls = session.lrange(name, start, end) or []
        return [data.decode() if isinstance(data, bytes) else data for data in data_ls]

    @classmethod
    def delete(cls, name):
        session = cls().get_session
        session.delete(name)
