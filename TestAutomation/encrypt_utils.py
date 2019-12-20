"""
工具类：常见加密算法

"""


import hashlib
import base64
from urllib import parse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings


serializer = Serializer(settings.SECRET_KEY, 300)		# serializer = Serializer(秘钥, 有效期秒)


def md5_encrypt(str):
    """md5加密"""
    md5 = hashlib.md5()
    # sha = hashlib.sha256()
    md5.update(str.encode("utf-8"))
    str_pass = md5.hexdigest()
    return str_pass


def sha_encrypt(str):
    """sha加密"""
    sha = hashlib.sha256()
    sha.update(str.encode("utf-8"))
    str_pass = sha.hexdigest()
    return str_pass


def base64_encrypt(str):
    return base64.b64encode(str)


def base64_decrypt(str_pass):
    return base64.b64decode(str_pass)


def url_encrypt(str):
    return parse.quote(str)


def url_decrypt(str_pass):
    return parse.unquote('str_pass')


def token_encrypt(str_dict):
    token = serializer.dumps(str_dict)  # serializer.dumps(数据), 返回bytes类型
    token = token.decode()
    return token


def token_decrypt(token):
    try:
        data = serializer.loads(token)
    except Serializer.BadData:  # 验证失败，会抛出itsdangerous.BadData异常
        return None
    else:
        return data