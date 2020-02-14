from selenium import webdriver
from TestAutomation.utils.redis_util import RedisOpt
import os

"""
浏览器驱动引擎
"""


class BrowserEngine(object):
    @classmethod
    def get_driver(self):
        '''根据浏览器配置获取对应的driver驱动'''
        driver = None
        browser_name = RedisOpt.get_str('ui_param_DriverType')
        driver_path = os.getcwd()+"/web_auto/drivers/"
        if browser_name == "Chrome":
            driver = webdriver.Chrome(executable_path=driver_path+"chromedriver.exe")
        elif browser_name == "Firefox":
            driver = webdriver.Firefox(executable_path=driver_path+"geckodriver.exe")
        elif browser_name == "Ie":
            driver = webdriver.Ie(executable_path=driver_path+"IEDriverServer.exe")
        flag = RedisOpt.get_str('ui_param_IfMaxWindow')
        if flag=='1':
            driver.maximize_window()
        implicitly_wait = RedisOpt.get_str('ui_param_ImplicitlyWait')
        driver.implicitly_wait(int(implicitly_wait))
        return driver


