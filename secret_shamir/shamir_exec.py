import secrets
from typing import List
from secret_shamir.shamir import combine_mnemonics, generate_mnemonics

'''
create函数使用范例
from secret_shamir import my_shamir as shamir_cli

temp = shamir_cli.create('3of5', 0, '65190580aaba3b0c674eb266d03cd6fa', 160)
返回值为所有密钥的list
'''
def create(
    scheme: str,            #scheme填需要分发多少个密钥，最少几人到场，密钥最大数为16
    exponent: int,          #迭代指数，到16就无法正常运算出结果，填0即可
    master_secret: str,     #主密码，输入32位的16进制数(即128位2进制数)
    strength: int,          #加密强度，必须大于主密码的二进制位数，默认为128，必须大于128
) -> None:
    if "of" in scheme:
        m, n = map(int, scheme.split("of", maxsplit=1))
        threshold = 1
        groups = [(m, n)]

    if master_secret is not None:
        secret_bytes = fill_string(master_secret).encode()
    else:
        secret_bytes = secrets.token_bytes(strength // 8)

    passphrase_bytes = b""
    mnemonics = generate_mnemonics(
        threshold, groups, secret_bytes, passphrase_bytes, exponent
    )

    for i, (group, (m, n)) in enumerate(zip(mnemonics, groups)):
        pass
    return group


'''
输入刚好满足解密条件长度的密语list，返回值为明文
shamir_cli.recover(my_list)
'''
def recover(all_mnemonics: List) -> None:
    passphrase_bytes=b''
    master_secret = combine_mnemonics(all_mnemonics, passphrase_bytes)
    return erase_string(master_secret.decode())


def fill_string(string: str):
    while len(string)<16:
        string += '\0'
    return string


def erase_string(string: str):
    string_return = string.replace('\0', '')
    return string_return
