import socket
from threading import Thread
from time import sleep
import simplejson
import compareDatabase

PORT = 8712
MAX_CLIENT = 5

ADDRESS = ('0.0.0.0', PORT)  # 绑定地址
g_socket_server = None  # 负责监听的socket
g_conn_pool = []  # 连接池


# 初始化服务端
def init():
    global g_socket_server
    g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
    g_socket_server.bind(ADDRESS)
    g_socket_server.listen(MAX_CLIENT)  # 最大等待数
    print("服务端已启动，等待客户端连接...")


# 接收新连接
def accept_client():
    while True:
        client, _ = g_socket_server.accept()  # 阻塞，等待客户端连接
        g_conn_pool.append(client)  # 加入连接池
        thread = Thread(target=message_handle, args=(client,))  # 给每个客户端创建一个独立的线程进行管理
        thread.setDaemon(True)  # 设置成守护线程
        thread.start()


# 消息处理函数
def message_handle(client):
    """
    消息处理
    """
    client.sendall("连接服务器成功!".encode())
    while True:
        recv_message = client.recv(1024).decode(encoding="utf8")
        if len(recv_message) != 0:
            print(recv_message)
            dic = simplejson.loads(recv_message)
            if compareDatabase.compare_password(dic['user'], dic['password']):
                print('password correct')
                client.sendall('correct'.encode())
            else:
                print('password incorrect')
                client.sendall('incorrect'.encode())
        else:
            client.close()
            g_conn_pool.remove(client)  # 删除连接
            print("Client Disconnect")
            break


init()
thread = Thread(target=accept_client)  # 新开一个线程，用于接收新连接
thread.setDaemon(True)
thread.start()
# 主线程逻辑
while True:
    sleep(1)

'''while True:
    cmd = input('--------------------------\n'
                '输入1:查看当前在线人数\n'
                '输入2:给指定客户端发送消息\n'
                '输入3:关闭服务端\n')
    if cmd == '1':
        print("--------------------------")
        print("当前在线人数：", len(g_conn_pool))
        for client in g_conn_pool:
            print(client.getpeername())
    elif cmd == '2':
        print("--------------------------")
        index, msg = input("请输入“索引,消息”的形式：").split(",")
        g_conn_pool[int(index)].sendall(msg.encode(encoding='utf8'))
    elif cmd == '3':
        exit()
'''
