# -*- coding: utf-8 -*-
import base64
import string

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import secrets


def create_aes_key(length=32, contain_punctuation=False):
    """
    生成key
    :return:
    """
    # 是否包含标点符号,默认是大小写+数字
    if contain_punctuation:
        characters = string.ascii_letters + string.digits + string.punctuation
    else:
        characters = string.ascii_letters + string.digits

    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string

class AES_ECB:
    def __init__(self, key):
        # 初始化密钥
        self.key = key
        # 初始化数据块大小
        self.length = AES.block_size
        # 初始化AES,ECB模式的实例
        self.aes = AES.new(self.key.encode("utf-8"), AES.MODE_ECB)
        # 截断函数，去除填充的字符
        self.unpad = lambda date: date[0:-ord(date[-1])]



    def fill_method(self, aes_str):
        """
        pkcs7补全-加密字符串也需要16的倍数，这里用PKCS-7规则补齐
        :param aes_str:
        :return:
        """
        pad_pkcs7 = pad(aes_str.encode('utf-8'), AES.block_size, style='pkcs7')

        return pad_pkcs7

    def encrypt(self, message):
        """
        AES加密
        :param encrData: 要加密的字符串
        :return:
        """
        # 加密函数,使用pkcs7补全
        res = self.aes.encrypt(self.fill_method(message))
        # 转换为base64
        msg = str(base64.b64encode(res), encoding="utf-8")

        return msg

    def decrypt(self, decrData):
        """
        AES解密
        :param decrData: 要解密的字符串
        :return:
        """
        # base64解码
        res = base64.decodebytes(decrData.encode("utf-8"))
        # 解密函数
        msg = self.aes.decrypt(res).decode("utf-8")

        return self.unpad(msg)


if __name__ == '__main__':

    # 生成aes加密key
    key = create_aes_key()
    print(key)

    eg = AES_ECB(key)
    # AES加密
    en = eg.encrypt("测试数据")
    print("加密结果：{}".format(en))

    # AES解密
    de = eg.decrypt(en)
    print("解密结果：{}".format(de))
