from selenium import webdriver
from TestAutomation.utils.redis_util import RedisOpt
import os
from selenium.webdriver.chrome.options import Options

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
        else:
            chrome_opt = Options()  # 创建参数设置对象，等同：chrome_opt = webdriver.ChromeOptions()
            chrome_opt.add_argument("--headless")  # 无界面化.
            chrome_opt.add_argument("--disable-gpu")  # 配合上面的无界面化，如果不加的话有时定位会有问题.
            chrome_opt.add_argument("service_args = [’–ignore - ssl - errors = true’, ‘–ssl - protocol = TLSv1’]")
            driver = webdriver.Chrome(executable_path=driver_path+"chromedriver.exe",options=chrome_opt)    # 创建Chrome对象并传入设置信息.
        flag = RedisOpt.get_str('ui_param_IfMaxWindow')
        if flag=='1':
            driver.maximize_window()
        implicitly_wait = RedisOpt.get_str('ui_param_ImplicitlyWait')
        driver.implicitly_wait(int(implicitly_wait))
        base_url = RedisOpt.get_str('ui_param_BaseUrl')
        driver.get(base_url)
        return driver


