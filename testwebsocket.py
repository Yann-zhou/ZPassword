from ssl_socket import myWebSocketServer

server1 = myWebSocketServer.Server(4200)
server2 = myWebSocketServer.Server(4200)

server1.start()