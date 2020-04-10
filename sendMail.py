import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import random
import hashlib


# 向输入的邮箱发送邮件，内容为随机8位字符串，返回值为该字符串的sha256值
def send_mail(receiver):
    my_sender = 'develop@zhouhongxin.com'  # 发件人邮箱账号
    my_pass = '-Zhx1998'  # 发件人邮箱密码
    my_user = receiver  # 收件人邮箱账号

    seed = "1234567890abcdefghijkmnpqrstuvwxyz"
    sa = []
    for i in range(8):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    print(salt)
    salt_sha256 = hashlib.sha256(salt.encode()).hexdigest()

    msg = MIMEText('您注册ZPassword所用的验证码为：'+salt, 'plain', 'utf-8')
    msg['From'] = formataddr(["ZPassword", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['To'] = formataddr([receiver, my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
    msg['Subject'] = "ZPassword注册验证"  # 邮件的主题，也可以说是标题

    server = smtplib.SMTP_SSL(host="smtp.exmail.qq.com", port=465)  # 发件人邮箱中的SMTP服务器
    server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
    server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件

    return salt_sha256
