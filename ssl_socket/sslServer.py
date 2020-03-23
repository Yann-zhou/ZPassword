import base64
import socket

import rsa
import hashlib
from sslError import AuthenticationError
import time
import simplejson
from ssl_socket import messageHandle
from Crypto.Cipher import AES
from Crypto import Random


class Server:
    # 用来标记同时连接的客户端的数量
    number = 0
    # 用来记录服务器接收到的消息
    receiver = None

    # 默认的最大等待数量为5
    # 默认使用本机的ip地址和8080端口
    def __init__(self, backlog=1, addr=('localhost', 8080)):
        # 默认使用AF_INET协议族，即ipv4地址和端口号的组合以及tcp协议
        self.serverSocket = socket.socket()
        # 绑定监听的ip地址和端口号
        self.serverSocket.bind(addr)
        # 开始等待
        self.serverSocket.listen(backlog)

        with open('public.pem') as publickfile:
            p = publickfile.read()
            self.publicKey = rsa.PublicKey.load_pkcs1(p)

    # 该函数需要并行处理
    def link_one_client(self):
        # 获取客户端对象和客户端地址
        clientSocket, addr = self.serverSocket.accept()

        # 客户端数量加1
        Server.number = Server.number + 1
        # 标记当前客户端编号
        now_number = Server.number

        # 打印
        print("和客户端{0}建立连接\n目标主机地址为：{1}".format(now_number, addr))

        # 下面是用公钥加密对称密钥并传递的过程
        # 产生用于对称加密的密钥
        aes_key = Random.get_random_bytes(32)
        # 偏移量vi取密钥的前16位
        aes_iv = aes_key[:AES.block_size]
        # 使用CBC模式加密
        aes_mode = AES.MODE_CBC
        # 用base64编码用来进行网络传输
        # 对密钥进行hash保证其准确性
        en_aes_key = base64.b64encode(rsa.encrypt(aes_key, self.publicKey))
        en_aes_key_sha256 = hashlib.sha256(en_aes_key).hexdigest()
        en_aes_key_json = {
            'en_aes_key': en_aes_key,
            'en_aes_key_sha256': en_aes_key_sha256
        }
        print("正在加密传送密钥")
        clientSocket.send(simplejson.dumps(en_aes_key_json).encode())

        # 这里可以添加密钥交换成功的函数

        # 初始化加密对象
        cryptor = AES.new(aes_key, aes_mode, aes_iv)

        # 下面使用对称密钥进行加密对话的过程
        try:
            while True:
                time.sleep(0.3)
                # 接收到的加密消息
                en_recv_data = base64.b64decode(clientSocket.recv(1024))
                # 去掉消息中的占位符
                recv_data = cryptor.decrypt(en_recv_data).decode().rstrip('\0')
                print("接收到客户端{0}传来的消息：{1}".format(now_number, recv_data))
                receiver = simplejson.loads(recv_data)

                # 处理消息并返回结果
                send_data = simplejson.dumps(messageHandle.message_handle(receiver['signal'], receiver['message']))

                # 对消息进行加密
                # 加密要传送的信息
                cipher_send_data = cryptor.encrypt(ciper_text(send_data))
                # 将加密后的信息进行base64编码
                en_send_data = base64.b64encode(cipher_send_data)
                clientSocket.send(en_send_data)
        except Exception as e:
            print('服务器出错！')
            print('错误信息：', e)
            print(now_number, '号客户端已断开')
            self.serverSocket.listen()


# 补全加密内容到16位
def ciper_text(content):
    length = 16
    count = len(content)
    if count % length != 0:
        add = length - (count % length)
    else:
        add = 0
    return content + ('\0' * add)