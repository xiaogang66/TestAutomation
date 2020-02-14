from web_auto.base_page import BasePage
from TestAutomation.utils.assert_util import AssertUtil
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as ec
from web_auto.browser_engine import BrowserEngine
from TestAutomation.utils.redis_util import RedisOpt


class RunCase(BasePage):
    """用例执行类"""
    # 定位方式
    LOCATE_TYPES = {1:By.ID,2:By.NAME,3:By.CSS_SELECTOR,4:By.XPATH,5:By.CLASS_NAME,6:By.TAG_NAME,7:By.LINK_TEXT}
    FRAME_LOCATE = 8
    WINDOW_LOCATE = 9

    # 元素操作方式
    CLICK_OPT = 1
    INPUT_OPT = 2
    DOUBLE_CLICK_OPT = 3
    MOVENO_OPT = 4
    CONTEXT_CLICK_OPT = 5
    SWITCH_OPT = 6

    # 断言方式
    ASSERT_VALUE_EQUAL = 1
    ASSERT_VALUE_CONTAIN = 2
    ASSERT_VALUE_REGULAR = 3
    ASSERT_TEXT_EQUAL = 4
    ASSERT_TEXT_CONTAIN = 5
    ASSERT_TEXT_REGULAR = 6

    # 用例执行结果
    CASE_PASS = 1
    CASE_NOT_PASS = 2
    CASE_EXCEPTION = 3

    def __init__(self,logger):
        self.driver = BrowserEngine.get_driver()
        self.base_page = BasePage(self.driver)
        self.assertUtil = AssertUtil()
        self.logger = logger
        base_url = RedisOpt.get_str('ui_param_BaseUrl')
        self.driver.get(base_url)

    def run_case_by_step(self,step):
        """执行用例步骤"""
        if step.step_type == 1:
            return self.run_element_step(step)
        elif step.step_type == 2:
            return self.run_assert_step(step)

    def run_element_step(self,step):
        """执行元素操作步骤"""
        try:
            self.logger.info('执行UI测试用例步骤：%s'% step.step_name)
            locate_type = step.element.locate_type
            locate_pattern = step.element.locate_partern
            operate_type = step.operate_type
            content = step.content
            if locate_type ==self.WINDOW_LOCATE:
                if operate_type == self.SWITCH_OPT:
                    # window窗口切换操作
                    self.base_page.switch_to_window_by_title(content)
                else:
                    pass
            elif locate_type ==self.FRAME_LOCATE:
                if operate_type == self.SWITCH_OPT:
                    # frame切换操作
                    if content == '':
                        self.base_page.default_frame()
                    elif content == '..':
                        self.base_page.parent_frame()
                    else:
                        self.base_page.switch_frame(content)
                else:
                    pass
            else:
                # 元素正常定位操作
                dest_element = self.base_page.util_locate_element(self.LOCATE_TYPES[locate_type], locate_pattern)
                if operate_type == self.CLICK_OPT:
                    self.base_page.util_click(self.LOCATE_TYPES[locate_type],locate_pattern)
                elif operate_type == self.INPUT_OPT:
                    self.base_page.util_send_keys(self.LOCATE_TYPES[locate_type],locate_pattern,content)
                elif operate_type == self.DOUBLE_CLICK_OPT:
                    self.base_page.double_click(dest_element)
                elif operate_type == self.MOVENO_OPT:
                    self.base_page.move_to_element(dest_element)
                elif operate_type == self.CONTEXT_CLICK_OPT:
                    self.base_page.right_click(dest_element)
                elif operate_type == self.SWITCH_OPT:
                    self.base_page.switch_frame(dest_element)
        except Exception as e:
            return [' ',3,e]
        return [' ',3,' ']

    def run_assert_step(self,step):
        """执行断言操作步骤"""
        case = step.case
        step_no = step.step_no
        step_name = step.step_name
        step_type = step.step_type
        element = step.element
        assert_type = step.assert_type
        assert_pattern = step.assert_partern
        locate_type = step.element.locate_type
        locate_pattern = step.element.locate_partern
        return self.assert_handle(locate_type,locate_pattern,assert_type,assert_pattern)

    def assert_handle(self, locate_type,locate_pattern, assert_type, assert_pattern):
        """根据断言方式进行断言判断"""
        try:
            real_result = ' '
            assert_flag = False
            time.sleep(3)
            element = self.base_page.util_locate_element(self.LOCATE_TYPES[locate_type], locate_pattern)
            element_text = element.get_attribute('innerHTML')
            element_value = element.get_attribute('value')
            if assert_type == self.ASSERT_VALUE_EQUAL:
                real_result = element_value
                self.logger.info("UI值相等断言，预期结果：%s，实际结果：%s" % (assert_pattern, element_value))
                assert_flag = self.assertUtil.equals(element_value, assert_pattern)
            elif assert_type == self.ASSERT_VALUE_CONTAIN:
                real_result = element_value
                self.logger.info("UI值包含断言，预期包含字段：%s，实际结果：%s" % (assert_pattern, element_value))
                assert_flag = self.assertUtil.contains(element_value, assert_pattern)
            elif assert_type == self.ASSERT_VALUE_REGULAR:
                real_result = element_value
                self.logger.info("UI值正则断言，预期正则：%s，实际结果：%s" % (assert_pattern, element_value))
                assert_flag = self.assertUtil.re_matches(element_value, assert_pattern)
            elif assert_type == self.ASSERT_TEXT_EQUAL:
                real_result = element_text
                self.logger.info("UI文本相等断言，预期结果：%s，实际结果：%s" % (assert_pattern, element_text))
                assert_flag = self.assertUtil.equals(element_text, assert_pattern)
            elif assert_type == self.ASSERT_TEXT_CONTAIN:
                real_result = element_text
                self.logger.info("UI文本包含断言，预期包含字段：%s，实际结果：%s" % (assert_pattern, element_text))
                assert_flag = self.assertUtil.contains(element_text, assert_pattern)
            elif assert_type == self.ASSERT_TEXT_REGULAR:
                real_result = element_text
                self.logger.info("UI文本正则断言，预期正则：%s，实际结果：%s" % (assert_pattern, element_text))
                assert_flag = self.assertUtil.re_matches(element_text, assert_pattern)
        except Exception as e:
             return [real_result, self.CASE_EXCEPTION, e]
        if assert_flag is True:
            return [real_result,self.CASE_PASS,' ']
        else:
            return [real_result, self.CASE_NOT_PASS, ' ']





