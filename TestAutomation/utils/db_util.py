from pymysql import Connection
from utils.configparam_util import ConfigEngine
import os

"""
数据库sql处理封装
"""


class MysqlDb(object):

    def __init__(self):
        configEngine = ConfigEngine()
        file_path = os.path.dirname(os.path.abspath("."))+"/SeleniumForPython/config/jdbc.ini"
        self.host = configEngine.get_param(file_path, 'dataBase', 'host')
        self.port = configEngine.get_param(file_path, 'dataBase', 'port')
        self.user = configEngine.get_param(file_path, 'dataBase', 'user')
        self.password = configEngine.get_param(file_path, 'dataBase', 'password')
        self.database = configEngine.get_param(file_path, 'dataBase', 'database')
        self.charset = configEngine.get_param(file_path, 'dataBase', 'charset')
        self.conn = Connection(host=self.host, port=int(self.port), user=self.user, password=self.password,database=self.database, charset=self.charset)
        self.cursor = self.conn.cursor()

    def query_one(self,sql,params=None):
        """执行查询数据语句"""
        self.cursor.execute(sql,params)
        return self.cursor.fetchone()

    def query_all(self,sql,params=None):
        """执行查询数据语句"""
        self.cursor.execute(sql,params=None)
        return self.cursor.fetchall()

    def update_or_delete(self,sql, params=None):
        """执行操作数据语句"""
        self.cursor.execute(sql, params=None)

    def roll_back(self):
        self.cursor.rollback()

    def commit(self):
        self.cursor.commit()
