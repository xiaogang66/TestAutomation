# _*_ coding: utf-8 _*_

"""
redis操作工具类
"""

from django_redis import get_redis_connection
import _pickle as pickler


class RedisOpt(object):
    """redis操作类"""

    conn = get_redis_connection("default")

    @classmethod
    def set(self,key,value):
        """添加数据"""
        self.conn.set(key, value)

    @classmethod
    def get(self,key):
        """获取数据"""
        return self.conn.get(key)

    @classmethod
    def get_str(self,key):
        """获取字符串数据"""
        result = self.conn.get(key)
        if result:
            return str(result, 'UTF-8')
        else:
            return None

    @classmethod
    def set_obj(self,key,obj):
        """对象序列化"""
        byte_data = pickler.dumps(obj, protocol=None, fix_imports=True)
        self.conn.set(key, byte_data)

    @classmethod
    def get_obj(self,key):
        """对象反序列化"""
        byte_data = self.conn.get(key)
        return pickler.loads(byte_data,fix_imports=True,encoding="ASCII",errors ="strict")

    @classmethod
    def delete(self,key):
        self.conn.delete(key)
