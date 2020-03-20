#from ssl_socket.sslclient import Client
from sslClient import Client

print("欢迎使用客户端程序！")
client = Client()
client.link_server()