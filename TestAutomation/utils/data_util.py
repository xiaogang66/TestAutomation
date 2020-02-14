# _*_ coding: utf-8 _*_

"""
数据处理类（数据格式转换、json解析）
"""
from jsonpath_rw import jsonpath,parse
import json


class DataUtil(object):

    def json_data_analysis(self,pattern,str_data):
        """根据表达式解析json数据"""
        dict_data = json.loads(str_data)
        json_exe = parse(pattern)
        madle = json_exe.find(dict_data)
        result = [math.value for math in madle]
        if result is None or result == []:
            return None
        else :
            return result[0]

    def dict_to_jsonstr(self, strs):
        """将字典转换为json字符串"""
        result = json.dumps(strs,ensure_ascii=False,sort_keyss=True,indent=2)
        return result

    def jsonstr_to_dict(self, jsons):
        """将json字符串转换为字典"""
        result = json.loads(jsons)
        return result

