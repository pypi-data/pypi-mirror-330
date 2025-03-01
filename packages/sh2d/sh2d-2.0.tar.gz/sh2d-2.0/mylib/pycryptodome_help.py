#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import base64
import binascii
from Crypto.Util.Padding import pad,unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import DES
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

def rsa_encrypt(msg, key, encoding='utf8'):
    public_key = RSA.importKey(key)
    cipher = PKCS1_cipher.new(public_key)
    encrypt_text = base64.b64encode(cipher.encrypt(msg.encode(encoding)))
    return encrypt_text.decode(encoding)

class DES_ECB:

    def __init__(self, key):

        key = key.encode('utf8')
        key = key[:8] if len(key) >= 8 else key + (8-len(key))*b'\0'
        self.cipher = DES.new(key, DES.MODE_ECB)

    def encrypt(self, text):
        ct = self.cipher.encrypt(pad(text.encode('utf8'), 8))
        return binascii.b2a_base64(ct).decode('utf8').strip()

    def decrypt(self, text):
        text = binascii.a2b_base64(text)
        ct = self.cipher.decrypt(text)
        return unpad(ct,8).decode('utf8').strip()