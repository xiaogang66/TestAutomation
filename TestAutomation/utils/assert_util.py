# _*_ coding: utf-8 _*_

"""
响应断言类
"""
import re


class AssertUtil(object):

    def equals(self,exp,result):
        """判断是否相等"""
        return exp == result

    def contains(self,result,target):
        """判断是否包含"""
        return target in result

    def re_matches(self,result,pattern):
        """判断是否匹配正则"""
        match =  re.match(pattern,result)
        if match is None:
            return False
        else:
            return True
