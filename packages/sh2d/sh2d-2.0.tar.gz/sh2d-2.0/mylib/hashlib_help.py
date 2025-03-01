# -*- coding: UTF-8 -*-

import hashlib
import secrets
from typing import Union


def md5(data: bytes) -> str:
    """
    计算字节数据的 MD5 哈希值。

    :param data: 输入的字节数据
    :return: MD5 哈希值的十六进制字符串
    """
    return hashlib.md5(data).hexdigest()


def sha1(data: bytes) -> str:
    """
    计算字节数据的 SHA1 哈希值。

    :param data: 输入的字节数据
    :return: SHA1 哈希值的十六进制字符串
    """
    return hashlib.sha1(data).hexdigest()


def sha256(data: bytes) -> str:
    """
    计算字节数据的 SHA256 哈希值。

    :param data: 输入的字节数据
    :return: SHA256 哈希值的十六进制字符串
    """
    return hashlib.sha256(data).hexdigest()


def generate_random_md5() -> str:
    """
    生成一个随机的 MD5 哈希值。

    :return: 随机生成的 MD5 哈希值的十六进制字符串
    """
    random_bytes = secrets.token_bytes(16)  # 生成 16 字节的随机数据
    return md5(random_bytes)


# 测试代码
if __name__ == "__main__":
    # 测试 md5
    text = b"Hello, World!"
    print(f"MD5 of text: {md5(text)}")
    # 测试 sha1
    print(f"SHA1 of text: {sha1(text)}")
    # 测试 sha256
    print(f"SHA256 of text: {sha256(text)}")
    # 测试 generate_random_md5
    print(f"Random MD5: {generate_random_md5()}")
