# _*_ coding: utf-8 _*_


"""
接口用例基础执行类（数据依赖处理、执行请求、结果解析）
"""
from interface_auto.models import InterfaceSuitExecuteRecord,InterfaceSuitCaseExecuteRecord
from sys_manager.models import Module
from interface_auto.request_util import  RequestUtil
from TestAutomation.utils.data_util import DataUtil
from TestAutomation.utils.assert_util import AssertUtil
from TestAutomation.utils.logger_util import Logger
from requests.cookies import RequestsCookieJar
from django.utils import timezone
import datetime
import re



class RunCase(object):

    CASE_RUN_FLAG = 1
    CASE_FORBID_FLAG = 0
    REQUEST_METHOD_GET = 1
    REQUEST_METHOD_POST = 2
    ASSERT_EQUAL = 1
    ASSERT_CONTAIN = 2
    ASSERT_REGULAR = 3
    CASE_SUCCESS = 1
    CASE_FAIL = 2
    CASE_EXCEPTION = 3
    JSON_CONTENT_TYPE = 1
    FORM_CONTENT_TYPE = 2

    def __init__(self,logger):
        self.requestUtil = RequestUtil()
        self.dataUtil = DataUtil()
        self.assertUtil = AssertUtil()
        self.logger = logger
        self.cookie_dict = {}

    def run_case_by_data(self, single_case, case_suit_record):
        """根据数据执行单个用例，传入case_suit_record时记录执行结果，否则不记录"""
        if case_suit_record:
            self.logger.info("执行用例集接口用例：%s-%s-%s" % (single_case.module.module_name, single_case.case_no, single_case.case_name))
        try:
            # 用例执行结果对象
            interface_suit_case_execute_record= InterfaceSuitCaseExecuteRecord()
            interface_suit_case_execute_record.start_time = datetime.datetime.now()
            interface_suit_case_execute_record.case_no = single_case.case_no
            interface_suit_case_execute_record.case_name = single_case.case_name
            interface_suit_case_execute_record.case_description = single_case.case_description
            interface_suit_case_execute_record.run_flag = single_case.run_flag
            interface_suit_case_execute_record.url = single_case.url
            interface_suit_case_execute_record.request_method = single_case.request_method
            interface_suit_case_execute_record.content_type = single_case.content_type
            interface_suit_case_execute_record.request_header = single_case.request_header
            interface_suit_case_execute_record.request_cookie = single_case.request_cookie
            interface_suit_case_execute_record.request_param = single_case.request_param
            interface_suit_case_execute_record.assert_type = single_case.assert_type
            interface_suit_case_execute_record.assert_partern = single_case.assert_partern
            interface_suit_case_execute_record.build_time = single_case.build_time
            interface_suit_case_execute_record.modify_time = single_case.modify_time
            module_name = Module.objects.get(id=single_case.module_id).module_name
            interface_suit_case_execute_record.module_name = module_name
            interface_suit_case_execute_record.builder = single_case.builder

            # 数据准备
            case_no = single_case.case_no
            run_flag = single_case.run_flag
            content_type = single_case.content_type
            if run_flag == self.CASE_FORBID_FLAG:
                self.logger.info("用例禁用未执行：%s-%s-%s" % (single_case.module.module_name, single_case.case_no, single_case.case_name))
                # 用例不执行
                return
            elif run_flag == self.CASE_RUN_FLAG:
                url = single_case.url
                request_method = single_case.request_method
                # 请求头处理
                headers = single_case.request_header
                if headers is None or headers == '':
                    headers = {}
                else:
                    headers = self.dataUtil.jsonstr_to_dict(headers)
                # cookie处理
                cookies = single_case.request_cookie
                if cookies:
                    # 进行cookie的解析处理，判断是否存在cookie依赖
                    depend_cookie = self.cookie_depend(cookies)
                    if depend_cookie is not None:
                        if type(depend_cookie) == RequestsCookieJar:
                            cookies = depend_cookie
                        elif depend_cookie== '':
                            cookies = {}
                        else:
                            cookies = self.dataUtil.jsonstr_to_dict(depend_cookie)
                request_param = single_case.request_param
                if request_param is not None and case_suit_record is not None:
                    # 处理请求参数依赖
                    request_param = self.data_depend(request_param,case_suit_record)
                assert_type = single_case.assert_type
                assert_pattern = single_case.assert_partern

                # 执行并记录结果
                # self.logger.info("请求URL：%s" % url)
                # self.logger.info("请求参数：%s" % request_param)
                # self.logger.info("请求头：%s" % headers)
                # self.logger.info("请求cookie：%s" % cookies)
                response = None
                if request_method == self.REQUEST_METHOD_GET:
                    self.logger.info("执行get接口，请求url:%s，请求参数:%s" % (url,request_param))
                    response = self.requestUtil.do_get(url,request_param,headers,cookies)
                elif request_method == self.REQUEST_METHOD_POST:
                    if content_type == self.JSON_CONTENT_TYPE:
                        # json请求
                        json_param = self.dataUtil.jsonstr_to_dict(request_param)
                        self.logger.info("执行post接口，请求url:%s，请求参数:%s" % (url, json_param))
                        response = self.requestUtil.do_post(url, json_param, None, headers, cookies)
                    elif content_type==self.FORM_CONTENT_TYPE:
                        # form请求
                        self.logger.info("执行post接口，请求url:%s，请求参数:%s" % (url, request_param))
                        headers["Content-Type"] = "application/x-www-form-urlencoded"
                        response = self.requestUtil.do_post(url, None, request_param, headers, cookies)
                response_text = response.text.strip()
                self.logger.info("接口请求结果：%s" % response_text)
                if case_no in self.cookie_dict:
                    self.cookie_dict[case_no] = response.cookies

                interface_suit_case_execute_record.status_code = response.status_code
                interface_suit_case_execute_record.real_result = response_text
                interface_suit_case_execute_record.end_time = datetime.datetime.now()

                # 断言判断，记录最终结果
                result = self.assert_handle(response_text,assert_type,assert_pattern)
                if result:
                    interface_suit_case_execute_record.pass_flag = self.CASE_SUCCESS
                else:
                    interface_suit_case_execute_record.pass_flag = self.CASE_FAIL
        except Exception as e:
            self.logger.info("接口执行异常：%s" % e)
            if case_suit_record is not None:
                interface_suit_case_execute_record.exception_msg = e
                interface_suit_case_execute_record.pass_flag = self.CASE_EXCEPTION
            else:
                return  {'msg':"用例执行异常，异常信息为：%s" % e}
        if case_suit_record is not None:
            interface_suit_case_execute_record.interface_suit_execute_record = case_suit_record
            interface_suit_case_execute_record.save()
        else:
            if result:
                return {'msg':"用例执行成功"}
            else:
                return {'msg':"用例执行失败，结果为：%s"%response_text}

    def data_depend(self,request_param,case_suit_record):
        """处理数据依赖
            ${test_03.data.orderId}   表示对返回结果的部分属性存在依赖
        """
        request_param_final = None
        # 处理返回结果属性依赖
        match_results = re.findall(r'\$\{.+?\..+?\}', request_param)
        if match_results is None or match_results == []:
            return request_param
        else:
            for var_pattern in match_results:
                self.logger.info("接口请求参数%s存在依赖：%s" % (request_param,var_pattern))
                # 只考虑匹配到一个的情况
                start_index  = var_pattern.index("{")
                end_index  = var_pattern.rindex("}")
                # 得到${}$中的值
                pattern = var_pattern[start_index+1:end_index]
                spilit_index = pattern.index(".")
                # 得到依赖的case_no和属性字段
                case_no = pattern[:spilit_index]
                proper_pattern = pattern[spilit_index+1:]
                interface_suit_case_execute_record = InterfaceSuitCaseExecuteRecord.objects.filter(interface_suit=case_suit_record)
                interface_suit_case_execute_record = interface_suit_case_execute_record.get(case_no=case_no)
                response = interface_suit_case_execute_record.real_result
                result = self.dataUtil.json_data_analysis(proper_pattern,response)
                # 参数替换，str(result)进行字符串强转，防止找到的为整数
                request_param_final = request_param.replace(var_pattern,str(result),1)
            return request_param_final

    def cookie_depend(self,request_param):
        """处理数据依赖
            1、${test_01}                表示对返回cookie存在依赖
            2、${test_03.data.orderId}   表示对返回结果的部分属性存在依赖
        """
        cookie_final = None
        # 处理对返回cookie的依赖
        match_results = re.match(r'^\$\{(.[^\.]+)\}$', request_param)
        if match_results:
            # 用例返回cookie依赖
            depend_cookie = self.cookie_dict[match_results.group(1)]
            return depend_cookie
        else:
            # 非用例返回cookie依赖
            cookie_final = self.data_depend(request_param)
            return cookie_final

    def assert_handle(self,response_text,assert_type,assert_pattern):
        """根据断言方式进行断言判断"""
        assert_flag = None
        if assert_type == self.ASSERT_EQUAL:
            self.logger.info("接口相等断言，预期结果：%s，实际结果：%s" % (assert_pattern,response_text))
            assert_flag = self.assertUtil.equals(response_text,assert_pattern)
        elif assert_type == self.ASSERT_CONTAIN:
            self.logger.info("接口包含断言，预期包含字段：%s，实际结果：%s" % (assert_pattern, response_text))
            assert_flag = self.assertUtil.contains(response_text, assert_pattern)
        elif assert_type == self.ASSERT_REGULAR:
            self.logger.info("接口正则断言，预期正则表达式：%s，实际结果：%s" % (assert_pattern, response_text))
            assert_flag = self.assertUtil.re_matches(response_text, assert_pattern)
        return assert_flag

