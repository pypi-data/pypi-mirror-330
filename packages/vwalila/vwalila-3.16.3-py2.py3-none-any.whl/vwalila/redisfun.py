# -*- coding: utf-8 -*-

from redis import StrictRedis
import json
from .config import config
from log_exc import send_log_exc_request


class RedisFun(object):
    def __init__(self, redis_url):
        self.redis_conn = StrictRedis.from_url(redis_url, decode_responses=True)

    def set_val(self, k, v, sec):
        if isinstance(v, basestring):
            self.redis_conn.set(k, v, sec)
        elif isinstance(v, (list, dict)):
            self.redis_conn.set(k, json.dumps(v, ensure_ascii=False), sec)

    def get_key(self, k):
        try:
            return self.redis_conn.get(k)
        except Exception:
            send_log_exc_request({
                "log_for": "redis_connection",
                "log_type": "error",
                "memo": "connect redis error.",
            })
            raise

redisfun = None

try:
    redisfun = RedisFun(redis_url=config['redis'])
except Exception:
    send_log_exc_request({
        "log_for": "redis_connection",
        "log_type": "error",
        "memo": "connect redis error.",
    })

