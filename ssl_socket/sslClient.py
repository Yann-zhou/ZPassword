import socket
import rsa
import base64
from Crypto.Cipher import AES
import hashlib
from sslError import AuthenticationError
import simplejson


class Client:

    def __init__(self):
        # 读取私钥
        with open('private.pem') as privatefile:
            p = privatefile.read()
            self.privateKey = rsa.PrivateKey.load_pkcs1(p)

    def link_server(self, addr=('localhost', 8080)):
        # 创建socket通信对象
        # 默认使用AF_INET协议族，即ipv4地址和端口号的组合以及tcp协议
        clientSocket = socket.socket()
        # 默认连接服务器地址为本机ip和8080端口
        clientSocket.connect(addr)


        # 接受服务器传递的密钥并进行解密
        en_aes_key_json = simplejson.loads(clientSocket.recv(1024))
        en_aes_key = en_aes_key_json['en_aes_key']
        print('en_aes_key:', en_aes_key)
        en_aes_key_sha256 = en_aes_key_json['en_aes_key_sha256']
        if hashlib.sha256(en_aes_key.encode()).hexdigest() != en_aes_key_sha256:
            raise AuthenticationError("密钥被篡改！")
        else:
            self.aes_key = rsa.decrypt(base64.b64decode(en_aes_key), self.privateKey)
            print("密钥交换完成")

        # 偏移量vi取密钥的前16位
        aes_iv = self.aes_key[:AES.block_size]
        # 使用CBC模式加密
        aes_mode = AES.MODE_CBC
        # 初始化加密对象
        cryptor = AES.new(self.aes_key, aes_mode, aes_iv)

        while True:
            # sendData = input("输入你要发送的消息：")
            json_data = {
                'signal': 2,
                'message': ['gvsrehw4w5ha3GW4_@123.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3']
            }
            send_data = simplejson.dumps(json_data)
            input('要发送的消息为：' + str(send_data) + '按任意键继续')

            # 对消息进行加密
            # 补全加密内容到16位
            length = 16
            count = len(send_data)
            if count % length != 0:
                add = length - (count % length)
            else:
                add = 0
            send_data = send_data + ('\0' * add)
            # 加密要传送的信息
            cipher_send_data = cryptor.encrypt(send_data.encode())
            # 将加密后的信息进行base64编码
            en_send_data = base64.b64encode(cipher_send_data)
            clientSocket.send(en_send_data)

            en_recv_data = base64.b64decode(clientSocket.recv(1024))
            # 解密并去掉消息中的占位符
            recv_data = simplejson.loads(cryptor.decrypt(en_recv_data).decode().rstrip('\0'))
            print("接受到服务器传来的消息：{0}".format(recv_data))
