import socket
import base64
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5

from ast import literal_eval


def rsa_long_encrypt(msg, length=200):
    """
    单次加密串的长度最大为 (key_size/8)-11
    1024bit的证书用100， 2048bit的证书用 200
    """
    recipient_key = RSA.import_key(
        open("public.pem").read()
    )
    rsa = PKCS1_v1_5.new(recipient_key)
    res = []
    for i in range(0, len(msg), length):
        print(len(msg))
        print(i)
        res.append(base64.b64encode(rsa.encrypt(msg[i:i+length].encode())).decode())
    return res


def rsa_long_decrypt(msg):
    recipient_key = RSA.import_key(
        open("private.pem").read()
    )
    rsa = PKCS1_v1_5.new(recipient_key)
    res = []
    msg = literal_eval(base64.b64decode(msg).decode())
    for i in msg:
        res.append(rsa.decrypt(base64.b64decode(i.encode()), None).decode("utf-8", "ignore"))
    return "".join(res)


def socket_send(socket_msg: str):
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect(('localhost', 4201))

    en_message = base64.b64encode(str(rsa_long_encrypt(socket_msg)).encode())
    socket_client.send(en_message)

    socket_recv = socket_client.recv(4096)
    socket_client.close()
    return socket_recv


