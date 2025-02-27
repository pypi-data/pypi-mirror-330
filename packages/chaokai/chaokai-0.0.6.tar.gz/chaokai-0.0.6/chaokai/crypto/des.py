# -*- coding: utf-8 -*-
import base64
import secrets
import string

from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad
from Cryptodome.Util.Padding import unpad


def create_des_key(length=24, contain_punctuation=False):
    """
    生成key，长度需8的倍数
    :return:
    """
    # 是否包含标点符号,默认是大小写+数字
    if contain_punctuation:
        characters = string.ascii_letters + string.digits + string.punctuation
    else:
        characters = string.ascii_letters + string.digits

    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string


def create_des_iv(contain_punctuation=False):
    """
    生成偏移量，长度必须为8
    :return:
    """
    length = 8
    # 是否包含标点符号,默认是大小写+数字
    if contain_punctuation:
        characters = string.ascii_letters + string.digits + string.punctuation
    else:
        characters = string.ascii_letters + string.digits

    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string


class DES3_CBC:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def fill_method(self, aes_str):
        """
        pkcs7补全-加密字符串也需要16的倍数，这里用PKCS-7规则补齐
        :param aes_str:
        :return:
        """
        pad_pkcs7 = pad(aes_str.encode('utf-8'), DES3.block_size, style='pkcs7')

        return pad_pkcs7

    def strip_method(self, data):
        """
        解密后的数据需要去除填充
        :param data:
        :return:
        """
        return unpad(data, DES3.block_size)

    def encrypt(self, encry_str):
        """
        :param key: 密钥需8倍数
        :param iv: 偏移量，必须为8
        :param encry_str:要加密的字符串
        :return:
        """
        key = self.key.encode('utf-8')
        iv = self.iv.encode('utf-8')

        cipher = DES3.new(key=key, mode=DES3.MODE_CBC, iv=iv)
        result = cipher.encrypt(self.fill_method(encry_str))
        return base64.b64encode(result).decode()

    def decrypt(self, encry_base64):
        """
        解密
        :param encry_base64: 需要解密的字符串
        :return:
        """
        encrypted_data = base64.b64decode(encry_base64)
        cipher = DES3.new(key=self.key, mode=DES3.MODE_CBC, iv=self.iv.encode())
        decrypted_data = cipher.decrypt(encrypted_data)

        # 去除填充并解码回字符串
        return self.strip_method(decrypted_data).decode('utf-8')


if __name__ == '__main__':
    key = create_des_key()
    iv = create_des_iv()
    print(key)
    print(iv)

    des3 = DES3_CBC(key, iv)

    # 加密
    message = '哈哈哈'
    cryptStr = des3.encrypt(message)
    print(cryptStr)

    # 解密
    a = des3.decrypt(cryptStr)
    print(a)
