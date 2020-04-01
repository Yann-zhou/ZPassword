import binascii
import logging
from websocket_server import WebsocketServer
import base64
from Crypto.Cipher import AES
from Crypto import Random
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP, PKCS1_v1_5
import hashlib
import simplejson
from binascii import b2a_hex, a2b_hex, b2a_base64
import aes_en
import random


class Server:
    def __init__(self, port: int):
        # 老板rsa函数
        # 生成rsa密钥对
        '''(pubkey, privkey) = rsa.newkeys(2048)
        pub = pubkey.save_pkcs1()
        with open('public.pem', 'wb+')as f:
            f.write(pub)
        pri = privkey.save_pkcs1()
        with open('private.pem', 'wb+')as f:
            f.write(pri)'''
        # 读取密钥
        '''with open('public.pem', 'rb') as publickfile:
            p = publickfile.read()
            self.publicKey = rsa.PublicKey.load_pkcs1(p)
        with open('private.pem', 'rb') as privatefile:
            p = privatefile.read()
            self.privkey = rsa.PrivateKey.load_pkcs1(p)'''

        # 新版rsa函数
        # 生成密钥对
        # 值得注意的是，下方第二行函数的参数'pkcs'必须为1，否则前端js无法识别
        '''key = RSA.generate(2048)
        encrypted_key = key.exportKey(pkcs=1, protection="scryptAndAES256-CBC")
        with open("private.pem", "wb") as f:
            f.write(encrypted_key)
        with open("public.pem", "wb") as f:
            f.write(key.publickey().exportKey())'''

        recipient_key = RSA.import_key(
            open("public.pem").read()
        )
        self.rsa = PKCS1_v1_5.new(recipient_key)

        # 使用CBC模式加密
        self.aes_mode = AES.MODE_CBC

        self.server = WebsocketServer(port, host='', loglevel=logging.INFO)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_back)
        self.server.run_forever()

    def new_client(self, client, server):
        # 打印
        print("和客户端{0}建立连接\n目标主机地址为：{1}".format(client['id'], client['address']))

        # 产生用于对称加密的密钥
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        temp = []
        for i in range(32):
            temp.append(random.choice(seed))
        aes_key_de = ''.join(temp)
        print(aes_key_de)
        print(aes_key_de[:16])
        # 将上边所产生的32位随机字符串进行编码
        self.aes_key = aes_key_de.encode()
        # 偏移量iv取密钥的前16位
        self.aes_iv = aes_key_de[:16].encode()
        # 下面是用公钥加密对称密钥并传递的过程
        # 先将aes密钥转换为16进制
        # 之后对aes密钥进行rsa加密
        # 再用base64编码保证网络传输
        # 最后对密钥进行hash保证其准确性
        # en_aes_key = base64.b64encode(self.rsa.encrypt(aes_key))
        en_hex_aes_key = str(binascii.b2a_hex(self.aes_key))[2:-1]
        en_hex_aes_iv = str(binascii.b2a_hex(self.aes_iv))[2:-1]
        print(en_hex_aes_key)
        print(en_hex_aes_iv)
        en_aes_key = base64.b64encode(self.rsa.encrypt(en_hex_aes_key.encode()))
        en_aes_key_sha256 = hashlib.sha256(en_aes_key).hexdigest()
        en_aes_key_json = {
            'en_aes_key': en_aes_key,
            'en_aes_key_sha256': en_aes_key_sha256
        }
        print("正在加密传送密钥")
        server.send_message(client, simplejson.dumps(en_aes_key_json).encode())

    def client_left(self, client, server):
        pass

    def message_back(self, client, server, message):
        # 这里的message参数就是客户端传进来的内容
        print("Client(%d) said: %s" % (client['id'], message))
        # 这里可以对message进行各种处理
        result = "服务器已经收到消息了..." + message
        plain_text = aes_en.decrypt(self.aes_key, self.aes_iv, message)
        cipher_text = aes_en.encrypt(self.aes_key, self.aes_iv, "你好，我在。")
        print('接收到的客户端密文为：' + base64.b64decode(plain_text).decode())
        server.send_message(client, cipher_text)
        print('已发送服务器密文：'+str(cipher_text))

    def handle_login(self, text):
        pass
