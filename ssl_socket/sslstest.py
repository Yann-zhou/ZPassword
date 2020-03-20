import threading
from sslServer import Server
import os
import time
from queue import Queue

#服务器最大连接数，过大会导致内存占用过多
MAX_CONNECT = 2

print("欢迎使用服务端程序！")
print(os.getcwd())
server = Server()
while True:
    if threading.active_count() < MAX_CONNECT+1:
        # 这里使用多线程可以避免服务器阻塞在一个客户端上
        t = threading.Thread(target=server.link_one_client)
        t.start()
        print('已创建进程', t.name)
        print(threading.enumerate())
    time.sleep(1)