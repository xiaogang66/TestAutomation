# _*_ coding: utf-8 _*_

"""
redis操作工具类
"""

from django_redis import get_redis_connection

class RedisOpt(object):
    conn = get_redis_connection("default")

    @classmethod
    def set(self,key,value):
        self.conn.set(key, value)

    @classmethod
    def get(self,key):
        return self.conn.get(key)

    @classmethod
    def get_str(self,key):
        result = self.conn.get(key)
        if result:
            return str(result, 'UTF-8')
        else:
            return None

    @classmethod
    def delete(self,key):
        self.conn.delete(key)

