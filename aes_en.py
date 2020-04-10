import base64
from Crypto.Cipher import AES


def encrypt(key, iv, instr='\0'):
    mystr = _pad(instr)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ret = base64.b64encode(cipher.encrypt(mystr))
    return ret


def decrypt(key, iv, encrypted_data):
    encrypted_data = base64.b64decode(encrypted_data)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ret = _unpad(cipher.decrypt(encrypted_data))
    return ret


def _pad(s):
    BS = AES.block_size
    s = s.encode("utf-8")
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode("utf-8")


def _unpad(s):
    return s[:-ord(s[len(s) - 1:])]


def main():
    encryptedData = 'Zrq5Gvyu+GgWCDI5TI6r3g=='
    key = '1234567812345678'
    mystr = key
    iv = key

    print(encrypt(key, iv, mystr))
    print(decrypt(key, iv, encryptedData))


if __name__ == '__main__':
    main()
