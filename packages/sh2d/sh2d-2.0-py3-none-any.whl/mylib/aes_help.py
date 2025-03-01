# -*- coding: UTF-8 -*-

from Crypto.Cipher import AES


class AEScryptor:
    """
    AES 加解密工具类，支持多种填充模式和加密模式。
    输入输出均为字节格式（bytes）。
    """

    def __init__(self, key: bytes, mode: int, iv: bytes = b'', padding_mode: str = "PKCS7", key_length: int = 16):
        """
        初始化 AES 加解密工具
        :param key: 密钥，字节格式
        :param mode: 加密模式，支持 AES.MODE_CBC, AES.MODE_ECB, AES.MODE_CFB, AES.MODE_OFB, AES.MODE_CTR
        :param iv: 初始化向量（IV），字节格式，CBC/CFB/OFB 模式需要
        :param padding_mode: 填充模式，支持 "PKCS7", "ZeroPadding"
        :param key_length: 密钥长度，支持 16（128位）、24（192位）、32（256位）
        """
        self.key = key
        self.mode = mode
        self.iv = iv
        self.padding_mode = padding_mode
        self.key_length = key_length

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        对字节数据进行 AES 加密
        :param plaintext: 明文数据，字节格式
        :return: 加密后的数据，字节格式
        """
        # 填充数据
        padded_data = self._padding(plaintext)
        # 初始化 AES 对象
        cipher = self._init_aes()
        # 加密数据
        ciphertext = cipher.encrypt(padded_data)
        return ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        对字节数据进行 AES 解密
        :param ciphertext: 加密数据，字节格式
        :return: 解密后的数据，字节格式
        """
        # 初始化 AES 对象
        cipher = self._init_aes()
        # 解密数据
        padded_plaintext = cipher.decrypt(ciphertext)
        # 去除填充
        plaintext = self._strip_padding(padded_plaintext)
        return plaintext

    def _init_aes(self):
        """
        初始化 AES 对象
        :return: AES 对象
        """
        if self.mode in (AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB):
            return AES.new(self.key, self.mode, self.iv)
        elif self.mode == AES.MODE_ECB:
            return AES.new(self.key, self.mode)
        else:
            raise ValueError(f"Unsupported AES mode: {self.mode}")

    def _padding(self, data: bytes) -> bytes:
        """
        填充数据
        :param data: 原始数据，字节格式
        :return: 填充后的数据，字节格式
        """
        if self.padding_mode == "PKCS7":
            padding_length = self.key_length - (len(data) % self.key_length)
            return data + bytes([padding_length] * padding_length)
        elif self.padding_mode == "ZeroPadding":
            padding_length = self.key_length - (len(data) % self.key_length)
            return data + bytes([0] * padding_length)
        else:
            raise ValueError(f"Unsupported padding mode: {self.padding_mode}")

    def _strip_padding(self, data: bytes) -> bytes:
        """
        去除填充
        :param data: 填充后的数据，字节格式
        :return: 去除填充后的数据，字节格式
        """
        if self.padding_mode == "PKCS7":
            padding_length = data[-1]
            return data[:-padding_length]
        elif self.padding_mode == "ZeroPadding":
            return data.rstrip(b'\x00')
        else:
            raise ValueError(f"Unsupported padding mode: {self.padding_mode}")


# 示例代码
if __name__ == '__main__':
    # 示例：CBC 模式加密解密
    key = b"1234567890123456"  # 16 字节密钥
    iv = b"1234567890123456"   # 16 字节 IV
    plaintext = b"Hello, AES!"  # 待加密数据
    # 初始化 AEScryptor
    aes = AEScryptor(key=key, mode=AES.MODE_CBC, iv=iv, padding_mode="PKCS7")
    # 加密
    ciphertext = aes.encrypt(plaintext)
    print(f"Ciphertext: {ciphertext}")
    # 解密
    decrypted_text = aes.decrypt(ciphertext)
    print(f"Decrypted text: {decrypted_text}")
