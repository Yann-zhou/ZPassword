import socket

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 4201))
    sock.listen(5)
except:
    print("init socket error!")

while True:
    conn, addr = sock.accept()  # socket.accept()：返回(conn,address)对，其中conn是新的socket对象，在其上可以发送和接收数据；address是另一端的socket地址
    print(addr)

    conn.settimeout(5)
    szBuf = conn.recv(1024)  # 使用sock.accept()创建的socket对象，
    print("recv:", szBuf)

    if "0" == szBuf:
        conn.send('exit'.encode())
    else:
        conn.send('welcome client!'.encode());

    conn.close();
    print("end of sevice");