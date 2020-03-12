from web_auto.base_manager import BaseManager
from TestAutomation.utils.redis_util import RedisOpt
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from io import BytesIO
from PIL import Image, ImageEnhance
import pytesseract
import win32clipboard as w
import win32api
import win32con
import time


class BasePage(BaseManager):
    """
    浏览器常见操作
    键盘鼠标对象
    查找元素统一方法封装
    """

    def __init__(self,driver):
        self.driver = driver
        self.actionChains = ActionChains(driver)
        driver_wait_time = RedisOpt.get_str('ui_param_DriverWaitTime')
        poll_frequency = RedisOpt.get_str('ui_param_PollFrequency')
        self.wait = WebDriverWait(driver, int(driver_wait_time), float(poll_frequency))   # 最长等待时间

    def find_element(self,locate_type,locate_pattern):
        return self.driver.find_element(locate_type, locate_pattern)

    def find_element_by_expression(self,expression):
        """
       @param expression	定位表达式，根据第一个字符确定定位方式
            ".xxx"	根据className获取
            "<xxx"	根据css表达式获取
            "#xxx"	根据id获取
            "_xxx"	根据linkText获取
            "-xxx"	根据模糊linkText获取
            "@xxx"	根据name属性获取
            ">xxx"	根据xpath获取
            "xxx"	根据标签名获取
        @return	返回定位到的元素
        """
        element = None
        try:
            flag = expression.substring(0,1)
            realExpre = expression.substring(1, expression.length())
            if flag == ".":
                element = self.driver.find_element_by_class_name(realExpre)
            elif flag == "<":
                element = self.driver.find_element_by_css_selector(realExpre)
            elif flag == "#":
                element = self.driver.find_element_by_id(realExpre)
            elif flag == "_":
                element = self.driver.find_element_by_link_text(realExpre)
            elif flag == "-":
                element = self.driver.find_element_by_partial_link_text(realExpre)
            elif flag == "@":
                element = self.driver.find_element_by_name(realExpre)
            elif flag == ">":
                element = self.driver.find_element_by_xpath(realExpre)
            else:
                element = self.driver.find_element_by_tag_name(realExpre)
        except Exception as e:
            print(e)
        return element

    def find_subelement_by_expression(self,baseElement,expression):
        """
        根据表达式查找元素
        @param baseElement	基础页面对象
        @param expression	表达式
        @return				查找到的页面对象
        @throws Exception
        """
        element = None
        try:
            flag = expression.substring(0,1)
            realExpre = expression.substring(1, expression.length())
            if flag == ".":
                element = baseElement.find_element_by_class_name(realExpre)
            elif flag == "<":
                element = baseElement.find_element_by_css_selector(realExpre)
            elif flag == "#":
                element = baseElement.find_element_by_id(realExpre)
            elif flag == "_":
                element = baseElement.find_element_by_link_text(realExpre)
            elif flag == "-":
                element = baseElement.find_element_by_partial_link_text(realExpre)
            elif flag == "@":
                element = baseElement.find_element_by_name(realExpre)
            elif flag == ">":
                element = baseElement.find_element_by_xpath(realExpre)
            else:
                element = baseElement.find_element_by_tag_name(realExpre)
        except Exception as e:
            print(e)
        return element

    def get(self,url):
        """打开网址"""
        self.driver.get(url)

    def click(self,element):
        """按钮点击"""
        element.click()

    def send_keys(element,value):
        """文本框输入"""
        element.send_keys(value)

    def clear(self,element):
        """元素清空"""
        element.clear()

    def is_selected(self,element):
        """判断元素是否选中"""
        return element.isSelected()

    def is_enabled(self,element):
        """判断元素是否可用"""
        return element.isEnabled()

    def is_displayed(self,element):
        """判断元素是否显示"""
        return element.isDisplayed()

    def submit(self,element):
        """提交按钮类元素提交表单"""
        element.submit()

    def select_by_visibleText(self,selectElement,name):
        """根据选项名称下拉选择"""
        select = Select(selectElement)
        select.select_by_visible_text(name)

    def select_by_value(self,selectElement,value):
        """根据value值下拉选择"""
        select = Select(selectElement)
        select.select_by_value(value)

    def select_by_index(self,selectElement,index):
        """根据索引下表下拉选择"""
        select = Select(selectElement)
        select.select_by_index(index)

    def close(self):
        """关闭当前页面"""
        self.driver.close()

    def quit(self):
        """退出浏览器"""
        self.driver.quit()

    def forward(self):
        """网页前进"""
        self.driver.forward()

    def back(self):
        """网页后退"""
        self.driver.back()

    def get_current_url(self):
        """获取当前url"""
        return self.driver.current_url

    def get_title(self):
        """获取当前标题"""
        return self.driver.title

    def delete_all_cookies(self):
        """清除所有cookie"""
        self.driver.delete_all_cookies()

    def get_cookies(self):
        """获取所有cookies"""
        self.driver.get_cookies()

    def add_cookie(self,cookieName, cookieValue):
        """添加cookie"""
        cookieDict = {cookieName:cookieValue}
        self.driver.add_cookie(cookieDict)

    def time_sleep(self,seconds):
        """等待时间：秒"""
        time.sleep(seconds)

    def refresh(self):
        """页面刷新"""
        self.driver.refresh()

    def wait_page_refresh(self,element,refreshTime=10):
        """等待一段时间判断页面是否刷新，默认10秒"""
        isRefresh = False;
        i = 0
        try:
            while i < refreshTime:
                element.tag_name
                time.sleep(1)      # 每隔1秒获取一次标签
                i = i + 1
        except StaleElementReferenceException as e:
            isRefresh = True
            return isRefresh
        return isRefresh

    def switch_frame(self,frame):
        """根据id、name、索引切换frame"""
        self.driver.switch_to.frame(frame)

    def default_frame(self):
        """回到默认frame"""
        self.driver.switch_to.default_content()

    def parent_frame(self):
        """回到父级frame"""
        self.driver.switch_to.parent_frame()

    def switch_to_alert(self):
        """跳转并获取弹框alert"""
        return self.driver.switch_to.alert

    def accept_alert(self):
        """点击alert的确定按钮"""
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self):
        """点击取消和上面的关闭按钮"""
        self.driver.switch_to.alert.dismiss()

    def is_alert_exist(self):
        """判断弹窗是否存在"""
        try:
            self.driver.switch_to.alert
            return True
        except Exception as e:
            return False

    def deal_potential_alert(self,option):
        """处理一个潜在的弹窗:true表示点击确认，false表示点击取消"""
        flag = False
        alert = self.driver.switch_to.alert
        if alert == None:
            self.logger.info("There is no alert appear!")
        else:
            if option:
                alert.accept()
                self.logger.info("Accept the alert: " + alert.getText())
            else:
                alert.dismiss()
                self.logger.info("Dismiss the alert: " + alert.getText())
            flag = True
        return flag

    def switch_to_window(self):
        """适用于只弹出一个窗口的情况,直接切换到下一个窗口"""
        currentWindow = self.driver.current_window_handle        # 得到当前窗口的句柄
        handles = self.driver.window_handles
        for handle in handles:
            if currentWindow == handle:
                continue
            window = self.driver.switch_to.window(handle)
            self.logger.info("title=%s,url =%s" %(window.getTitle() ,window.getCurrentUrl()))

    def switch_to_window_by_title(self,title):
        pass

    def window_is_exist(self,windowTitle,defaultCount=5):
        """判断指定的窗口是否存在，最多遍历defaultCount次"""
        flag = False
        a = 0
        while a < defaultCount:
            windowHandles = self.driver.window_handles
            for handler in windowHandles:
                self.driver.switch_to.window(handler)
                title = self.driver.title
                if windowTitle == title:
                    flag = True
                    break
            a = a + 1
        return flag

    def move_to_element(self,element):
        """鼠标悬停事件"""
        self.actionChains.move_to_element(element).perform()

    def double_click(self,element):
        """鼠标双击"""
        self.actionChains.double_click(element).perform()

    def right_click(self,element):
        """鼠标右击"""
        self.actionChains.context_click(element).perform()

    def drag_by_element(self,source_element,target_element):
        """将按钮拖拽到指定元素"""
        self.actionChains.drag_and_drop(source_element, target_element).perform()

    def drag_by_offset(self,by,locate_pattern,x,y):
        """将按钮拖拽到具体坐标（x,y）"""
        element = self.wait.until(lambda driver: driver.find_element(by, locate_pattern))
        self.actionChains.drag_and_drop_by_offset(element,x,y).perform()

    def click_by_js(self,element):
        """利用js点击"""
        self.driver.execute_script("arguments[0].click()", element)

    def send_keys_by_js(self,element, content):
        """利用js输入文本"""
        self.driver.execute_script("arguments[0].value=arguments[1]", element, content)

    def alert_by_js(self,message):
        """给出指定信息的弹框"""
        self.driver.execute_script("alert('" + message + "')")

    def get_ready_state_by_js(self):
        """用js获取页面加载状态"""
        return self.driver.execute_script("return document.readyState")

    def get_title_by_js(self):
        """用js得到页面title"""
        return self.driver.execute_script("return document.title")

    def get_attr_by_js(self,element,attrName):
        """用js获取标签属性"""
        self.driver.execute_script("arguments[0].getAttribute(arguments[1])", element, attrName)

    def set_attr_by_js(self,element, attrName, attrValue):
        """用js设置标签属性"""
        self.driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2])", element, attrName, attrValue)

    def remove_attr_by_js(self, element, attrName):
        """用js移除标签属性"""
        self.driver.execute_script("arguments[0].removeAttribute(arguments[1])", element, attrName)

    def scroll_into_view( self,element):
        """元素滚动到浏览器窗口的可视区域内"""
        self.driver.execute_script("arguments[0].scrollIntoView()", element)

    def scroll(self, x, y):
        """网页滚动条移动(x,y)"""
        self.driver.execute_script("scroll(arguments[0],arguments[1])", x, y)

    def window_scroll_to_bottom(self):
        """窗口滚动到底部"""
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    def windowScrollToTop(self):
        """窗口滚动到顶部"""
        self.driver.execute_script("window.scrollTo(0,0)")

    def element_scroll_y(self,element,y):
        """元素纵向滚动"""
        self.driver.execute_script("arguments[0].scrollTop=arguments[1]", element, y)

    def element_scroll_x(self,element,x):
        """元素横向滚动"""
        self.driver.executeScript("arguments[0].scrollLeft=arguments[1]", element, x)

    def current_element_key_enter(self):
        """当前焦点元素回车"""
        self.driver.switch_to.active_element.send_keys(Keys.ENTER)

    def util_locate_element(self,by,locate_pattern):
        """元素被加载后返回该元素"""
        locate = (by, locate_pattern)
        return self.wait.until(ec.presence_of_element_located(locate))

    def util_click(self,by,locate_pattern):
        """按钮点击"""
        self.wait.until(lambda driver:driver.find_element(by,locate_pattern)).click()

    def util_send_keys(self,by,locate_pattern,value):
        """文本框输入"""
        self.wait.until(lambda driver: driver.find_element(by,locate_pattern)).send_keys(value)

    def util_clear(self,by,locate_pattern):
        """元素清空"""
        self.wait.until(lambda driver: driver.find_element(by,locate_pattern)).clear()

    def key_down(self,keyCode):
        """键盘按下"""
        win32api.keybd_event(keyCode, 0, 0, 0)

    def key_up(self,keyCode):
        """键盘抬起"""
        win32api.keybd_event(keyCode, 0, win32con.KEYEVENTF_KEYUP, 0)

    def key_enter(self):
        """键盘回车"""
        self.key_down(Keys.ENTER)
        self.key_up(Keys.ENTER)

    def key_copy(self, content):
        """复制文本后粘贴并回车，常用于拷贝文件路径"""
        # 1、内容设置到剪切板
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_UNICODETEXT, content)
        w.CloseClipboard()
        # 2、按下ctrl+v
        VK_CODE = {
            'enter': 0x0D,
            'ctrl': 0x11,
            'v': 0x56}
        self.key_down(VK_CODE['ctrl'])
        self.key_down(VK_CODE['v'])
        self.key_up(VK_CODE['ctrl'])
        self.key_up(VK_CODE['v'])

    def get_code_by_enhance(self, imgElement):
        """获取图片验证码"""
        screenImg = "D:/verifyCode.png"     # 验证码图片保存地址
        self.driver.get_screenshot_as_file(screenImg)            # 浏览器页面截图

        # 定位验证码大小
        location = imgElement.location
        size = imgElement.size
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        # 从文件读取截图，截取验证码位置再次保存
        img = Image.open(screenImg).crop((left, top, right, bottom))
        img.convert('L')  # 转换模式：L|RGB
        img = ImageEnhance.Contrast(img)  # 增加对比度
        img = img.enhance(2)  # 增加饱和度
        img.save(screenImg)

        # 再次读取验证码
        img = Image.open(screenImg)
        time.sleep(1)
        code = pytesseract.image_to_string(img,lang="eng")
        return code

    def get_code_by_erzhi(self,code_element,erzhi_color_code):
        """获取定位元素的验证码"""
        image_location = code_element.location      # 获取验证码在画布中的位置
        image_size = code_element.size
        # 截取页面图像并截取掩码码区域图像
        image = self.driver.get_screenshot_as_png()
        im = Image.open(BytesIO(image))
        imag_code = im.crop((image_location['x'], image_location['y'], image_location['x']+image_size['width'], image_location['y']+image_size['height']))  # 从截屏中获取图片大小的图像
        im_erzhihua = self.erzhihua(imag_code, erzhi_color_code)
        result = pytesseract.image_to_string(im_erzhihua, lang='eng')
        return result

    def erzhihua(self,image, threshold):
        """图片二值化"""
        image = image.convert('L')
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        return image.point(table, '1')

if __name__ == "__main__":
    page = BasePage()
    page.driver.get("http://172.21.201.85:7776/ent/login")
    codeElement = page.driver.find_element_by_id("imgVerify")
    code1 = page.get_code_by_erzhi(codeElement,100)
    code2 = page.get_code_by_enhance(codeElement)
    print("code1:%s"%code1)
    print("code2:%s"%code2)