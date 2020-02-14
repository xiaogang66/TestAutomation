# _*_ coding: utf-8 _*_

"""
请求处理类（get和post请求）
"""
import requests
from TestAutomation.utils.redis_util import RedisOpt


class RequestUtil(object):

    def do_get(self,url,params='',headers={},cookies={}):
        """get请求处理"""
        requests.packages.urllib3.disable_warnings()
        timeout = RedisOpt.get_str('interface_param_TimeOut')
        response = requests.get(url,params,verify=False,headers=headers,cookies=cookies,timeout=int(timeout))
        response.encoding = response.apparent_encoding
        return response

    def do_post(self,url,json=None,data=None,headers={},cookies={}):
        """post请求处理，传入json参数或普通参数"""
        requests.packages.urllib3.disable_warnings()
        timeout = RedisOpt.get_str('interface_param_TimeOut')
        response = None
        if json is not None:
            response = requests.post(url,json=json,verify=False,headers=headers,cookies=cookies,timeout=int(timeout))
        elif data is not None:
            response = requests.post(url,data=data,verify=False,headers=headers,cookies=cookies,timeout=int(timeout))
        response.encoding = response.apparent_encoding
        return response

