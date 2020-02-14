"""
文件和目录操作类
"""

import os
import datetime
from TestAutomation.utils.redis_util import RedisOpt


class FileUtil(object):

    @classmethod
    def list_all(self,path):
        """返回所有文件或目录列表"""
        file_names = os.listdir(path)
        file_names.sort(key=lambda x: int(x[3:10]))
        file_names.reverse()
        return file_names

    @classmethod
    def list_all_files(self,path):
        """返回所有文件列表"""
        file_names = os.listdir(path)
        for file_name in file_names:
            if self.is_file(path+'/'+file_name):
                pass
            else:
                file_names.remove(file_name)
        file_names.sort(key=lambda x: str(x[3:10]))
        file_names.reverse()
        return file_names

    @classmethod
    def list_all_dirs(self,path):
        """返回所有目录列表"""
        file_names = os.listdir(path)
        for file_name in file_names:
            if self.is_dir(path+'/'+file_name):
                pass
            else:
                file_names.remove(file_name)
        file_names.sort(key=lambda x: int(x[3:10]))
        file_names.reverse()
        return file_names

    @classmethod
    def make_dirs(path):
        """递归创建文件夹"""
        os.makedirs(path)

    @classmethod
    def make_dir(self,path):
        """创建文件夹"""
        os.mkdir(path)

    @classmethod
    def remove_file(self,path):
        """删除文件"""
        os.remove(path)

    @classmethod
    def remove_dirs(self,path):
        """递归删除目录"""
        os.removedirs(path)

    @classmethod
    def rename_file(self,src,dst):
        """文件更名"""
        os.rename(src, dst)

    @classmethod
    def renames_file(self,old,new):
        """递归更名"""
        os.renames(old, new)

    @classmethod
    def file_is_exists(self,path):
        """判断路径是否存在"""
        return os.path.exists(path)

    @classmethod
    def get_last_visit_time(self,path):
        """返回最近访问时间（浮点型秒数）"""
        gettime = os.path.getatime(path)
        gettime = datetime.datetime.fromtimestamp(gettime)
        return gettime.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def get_last_modify_time(self,path):
        """返回最近文件修改时间"""
        gettime = os.path.getmtime(path)
        gettime = datetime.datetime.fromtimestamp(gettime)
        return gettime.strftime('%Y-%m-%d %H:%M:%S')


    @classmethod
    def get_create_time(self,path):
        """返回文件创建时间"""
        gettime = os.path.getctime(path)
        gettime = datetime.datetime.fromtimestamp(gettime)
        return gettime.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def get_file_size(self,path):
        """返回文件大小，如果文件不存在就返回错误"""
        size = os.path.getsize(path)
        # 根据单位返回大小
        file_size_unit = RedisOpt.get_str('sys_param_FileSizeUnit')
        if file_size_unit.upper() == 'K':
            size = int(size/1024)
        elif file_size_unit.upper() == 'M':
            size = int(size/1024/1024)
        return size

    @classmethod
    def is_file(self,path):
        """判断路径是否为文件"""
        return os.path.isfile(path)

    @classmethod
    def is_dir(self,path):
        """判断路径是否为目录"""
        return os.path.isdir(path)

