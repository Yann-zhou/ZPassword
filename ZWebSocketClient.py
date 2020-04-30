import json
from ws4py.client.threadedclient import WebSocketClient
from Crypto.Cipher import AES
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5


class CG_Client(WebSocketClient):
    def __init__(self, s):

        recipient_key = RSA.import_key(
            open("public.pem").read()
        )

        self.rsa = PKCS1_v1_5.new(recipient_key)

        # 使用CBC模式加密
        self.aes_mode = AES.MODE_CBC
        self.user_auth_key = {}

    def opened(self):
        req = '{"event":"subscribe", "channel":"eth_usdt.deep"}'
        self.send(req)

    def closed(self, code, reason=None):
        print("Closed down:", code, reason)

    def received_message(self, resp):
        resp = json.loads(str(resp))
        data = resp['message']
        if type(data) is dict:
            ask = data['asks'][0]
            print('Ask:', ask)
            bid = data['bids'][0]
            print('Bid:', bid)


if __name__ == '__main__':
    ws = None
    try:
        ws = CG_Client('ws://127.0.0.1:4200')
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()