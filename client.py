import socket  # 导入 socket 模块

s = socket.socket()  # 创建 socket 对象
s.connect(('192.168.50.82', 8712))
print(s.recv(1024).decode(encoding='utf8'))
s.send("连接了".encode('utf8'))
print(s.recv(1024).decode(encoding='utf8'))
input("")