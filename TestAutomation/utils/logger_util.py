# _*_ coding: utf-8 _*_
import logging
import time
import os

class Logger(object):
    def __init__(self,class_name,log_dir,log_console,log_level):
        current_time = time.strftime('%Y%m%d',time.localtime(time.time()))
        # 文件路径需要判断是否存在
        if os.path.exists(log_dir):
            pass
        else:
            os.makedirs(log_dir)
        log_name = log_dir+'/'+current_time+".log"
        # 根据传入的类名获取当前类的日志对象
        logger = logging.getLogger(class_name)
        # 设置日志格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')        # handler添加格式
        # logger添加handler
        if "file" in log_console:
            fh = logging.FileHandler(log_name,encoding='utf-8')
            fh.setLevel(logging.INFO)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        if "console" in log_console:
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(formatter)
            logger.addHandler(ch)

        final_leval = logging.NOTSET
        # fatal、error、warning、info、debug
        if log_level.lower() == "fatal":
            final_leval = logging.FATAL
        elif log_level.lower() == "error":
            final_leval = logging.ERROR
        elif log_level.lower() == "warning":
            final_leval = logging.WARNING
        elif log_level.lower() == "info":
            final_leval = logging.INFO
        elif log_level.lower() == "debug":
            final_leval = logging.DEBUG
        logger.setLevel(final_leval)
        self.logger = logger


