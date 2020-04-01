# coding=utf-8
import logging
from ssl_socket.websocket_server import WebsocketServer


# 因为考虑到传入的字符串有非英文字符，
# 所以手动设置编码，否则可能会报编码错误
# reload(sys)
# sys.setdefaultencoding('utf-8')


def new_client(client, server):
    print("Client(%d) has joined." % client['id'])
    print(client['address'])


def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


def message_back(client, server, message):
    # 这里的message参数就是客户端传进来的内容
    print("Client(%d) said: %s" % (client['id'], message))
    # 这里可以对message进行各种处理
    result = handle_login(message)
    # 将处理后的数据再返回给客户端
    server.send_message(client, result)


def handle_login(text):
    # 这里使用5个星号作为数据间的分隔符
    # 当然在JS中也可以使用更高级的JSON字符串
    # 但这里为了简单就没有拼接
    username = text.split('*****')[0]
    password = text.split('*****')[1]
    if username == '1@1' and password == '1':
        login_res = "Login success!\nWelcome my master " + username + ". ๑乛◡乛๑"
    else:
        login_res = "Login fail!\nYou are not my master.(..•˘_˘•..)"
    return login_res


server = WebsocketServer(4200, host='', loglevel=logging.INFO)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_back)
server.run_forever()