import socket
import rsa
import pickle
from cryptography.fernet import Fernet
import hashlib
from sslError import AuthenticationError
import time


class Server:
    # 用来标记同时连接的客户端的数量
    number = 0
    # 用来记录服务器接收到的消息
    receiver = [0, None]

    # 默认的最大等待数量为5
    # 默认使用本机的ip地址和8080端口
    def __init__(self, backlog=5, addr=('localhost', 8080)):
        # 默认使用AF_INET协议族，即ipv4地址和端口号的组合以及tcp协议
        self.serverSocket = socket.socket()
        # 绑定监听的ip地址和端口号
        self.serverSocket.bind(addr)
        # 开始等待
        self.serverSocket.listen(backlog)

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
        # 接受客户端传递的公钥
        # 这里可以加一个哈希函数检验公钥的正确性！
        # 运用pickle进行反序列化
        publicKeyPK, pubKeySha256 = pickle.loads(clientSocket.recv(1024))
        if hashlib.sha256(publicKeyPK).hexdigest() != pubKeySha256:
            self.receiver = (4, ['密钥被篡改！'])
            raise AuthenticationError("密钥被篡改！")
        else:
            publicKey = pickle.loads(publicKeyPK)
            print("已接受公钥")

        # 下面是用公钥加密对称密钥并传递的过程
        # 产生用于对称加密的密钥
        sym_key = Fernet.generate_key()
        # 用pickle进行序列化用来进行网络传输
        # 对密钥进行hash保证其准确性
        en_sym_key = rsa.encrypt(pickle.dumps(sym_key), publicKey)
        en_sym_key_sha256 = hashlib.sha256(en_sym_key).hexdigest()
        print("正在加密传送密钥")
        clientSocket.send(pickle.dumps((en_sym_key, en_sym_key_sha256)))

        # 这里可以添加密钥交换成功的函数

        # 初始化加密对象
        f = Fernet(sym_key)

        # 下面使用对称密钥进行加密对话的过程
        try:
            while True:
                time.sleep(0.3)
                # 接收到的加密消息
                en_recvData = clientSocket.recv(1024)
                recvData = f.decrypt(en_recvData).decode()
                print("接受到客户端{0}传来的消息：{1}".format(now_number, recvData))
                self.receiver = (4, [now_number, recvData])

                sendData = recvData
                # 对消息进行加密
                en_sendData = f.encrypt(sendData.encode())
                clientSocket.send(en_sendData)
        except:
            print('服务器解密出错！')
            print(now_number, '号客户端已断开')
            self.serverSocket.listen()

    # 将接收到客户端的消息推送至主程序并重置消息接收器
    def get_message(self):
        temp = self.receiver
        self.receiver = [0, None]
        return temp
