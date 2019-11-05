# -*- coding: utf-8 -*-
from pyDes import *
from Crypto.Cipher import AES
import rsa
import base64
import hashlib
import hmac

class Sig_Server(object):
    def __init__(self):
        self.sigModel = ['DES', '3DES', 'AES', 'RSA', 'MD5', 'SHA1', 'SHA256', 'HmacSHA1']

    # mode 模式 padding填充 iv偏移量
    def DesMode(self, key, mode, iv, pad, padmode, inputData):
        if len(key) / 8 != 1:
            return "key长度不符合要求"
        if len(inputData) % 8 != 0:
            return "输入值不合符要求"
        try:
            k = des(key, mode, iv, pad, padmode)
            d = k.encrypt(inputData)
        except Exception as e:
            return e
        else:
            return base64.b64encode(d)

    def DesMode2(self, key, mode, iv, pad, padmode, inputData):
        data = base64.b64decode(inputData)
        k = des(key, mode, iv)
        return k.decrypt(data=data, pad=pad, padmode=padmode)

    def des3_Mode(self ,key, mode, iv, pad, padmode, inputData):
        if len(key) != 24:
            if len(key) != 16: # Use DES-EDE2 mode
                raise ValueError("Invalid triple DES key size. Key must be either 16 or 24 bytes long")
        k = triple_des(key, mode, iv, pad, padmode)
        d = k.encrypt(inputData)
        return base64.b64encode(d)

    def des3_Mode2(self, key, mode, iv, pad, padmode, inputData):
        data = base64.b64decode(inputData)
        k = triple_des(key, mode, iv)
        return k.decrypt(data=data, pad=pad, padmode=padmode)

    def AES_mode(self, plaintext, key, mode, iv):
        BS = AES.block_size # aes数据分组长度为128 bit
        pad = lambda s: s + (BS - len(s) % BS) * chr(0)
        cryptor = AES.new(key, mode, iv)
        ciphertext = cryptor.encrypt(pad(plaintext))
        return base64.b64encode(ciphertext)

    def AES_mode2(self, ciphertext, key, mode, iv):
        ciphertext = base64.b64decode(ciphertext)
        ciphertext = ciphertext[AES.block_size:len(ciphertext)]
        cryptor = AES.new(key, mode, iv)
        plaintext = cryptor.decrypt(ciphertext)
        return plaintext.rstrip(chr(0))

    def rsa_mode(self, message, key):
        # 公钥加密
        return base64.b64encode(rsa.encrypt(message.encode(), key))

    def rsa_mode2(self, message, key):
        # 私钥解密
        key = base64.b64encode(message)
        return rsa.decrypt(message, key)

    def rsa_sig(self,  message, key, mode):
        # 私钥签名
        return base64.b64encode(rsa.sign(message.encode(), key, mode))

    def rsa_sig2(self,  message, signature, key):
        # 公钥验证
        return rsa.verify(message, signature, key)

    # 不可逆 加密
    def md5_mode(self, data):
        h1 = hashlib.md5()
        h1.update(data)
        res = h1.hexdigest()
        return base64.b64encode(res)

    # sha1
    def sha1_mode(self, data):
        hexData = hashlib.sha1(data).hexdigest()
        return base64.b64encode(hexData)

    # sha256
    def sha256_mode(self, data):
        hexData = hashlib.sha256(data).hexdigest()
        return base64.b64encode(hexData)

    # hmac
    def hmac_mode(self, key, data):
        myhmac = hmac.new(key)
        myhmac.update(data)
        res = myhmac.hexdigest()
        return base64.b64encode(res)

#if __name__ == '__main__':
    # t = Sig_Server()
    # des111 = t.DesMode(key="DESCRYPT", mode=CBC, iv="\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5, inputData="Please  ")
    # print t.DesMode2(key="DESCRYPT", mode=CBC, iv="\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5, inputData="i9LJc8zZBLKoOsnCH+9vNg==")
    # print(t.des3_Mode(key="DESCRYPTDESCRYPT", mode=CBC, iv="\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5, inputData="Please  "))
    # print t.des3_Mode2(key="DESCRYPTDESCRYPT", mode=CBC, iv="\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5, inputData="i9LJc8zZBLKoOsnCH+9vNg==")
    # print t.AES_mode(key=b'keyven__keyven__', mode=AES.MODE_CBC, iv='0000000000000000', plaintext='keyven:加油!')
    # print t.md5_mode("this is a md5 test")
    # print t.sha1_mode("this is a sha1 test")
    # print t.hmac_mode("test", "test")