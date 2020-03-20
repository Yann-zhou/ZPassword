import socket
import simplejson


s = socket.socket()  # 创建 socket 对象
s.connect(('192.168.2.2', 8712))
print(s.recv(1024).decode())
dic = {"user": "def", "password": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"}
st = simplejson.dumps(dic)
s.send(st.encode())
print(s.recv(1024).decode())