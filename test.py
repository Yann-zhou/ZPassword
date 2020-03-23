import base64
from Crypto.Cipher import AES
from Crypto import Random

message = '''{
    'nihao': 123321,
    'wphenhao': 32112332532
}
'''
# 随机生成256位的aes密钥
aes_key = Random.get_random_bytes(32)
print('key is:', aes_key)
# 偏移量vi取密钥的前16位
aes_iv = aes_key[:AES.block_size]
# 使用CBC模式加密
aes_mode = AES.MODE_CBC
# 生成加密类
cryptor = AES.new(aes_key, aes_mode, aes_iv)
# 补全加密内容到16位
length = 16
count = len(message)
if count % length != 0:
    add = length - (count % length)
else:
    add = 0
message = message + ('\0' * add)
# 对信息进行加密
ciphertext = cryptor.encrypt(message.encode())
# 将加密后的信息进行base64编码
result = base64.b64encode(ciphertext)
print(result)

# 生成解密类
cryptor = AES.new(aes_key, aes_mode, aes_iv)
# 对信息进行base64解密并进行aes解密
plain_text = cryptor.decrypt(base64.b64decode(result))
# 去掉信息中的占位符
print(plain_text.decode().rstrip('\0'))