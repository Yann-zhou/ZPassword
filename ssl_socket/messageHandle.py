from database_tool import userTable
from database_tool import detailTable

'''
消息处理函数，用来处理服务器接收到的消息
消息格式是[信号, 消息内容]
信号    信号含义    消息内容    返回值
 X    客户端发送公钥    ['公钥']    经公钥加密后的Fernet对称密钥
 1    客户端请求登录    ['用户名', '密码sha256值']    用户不存在或密码错误或登陆成功及数据库内容
 2    客户端请求增加用户    ['用户名', '密码sha256值']    用户已存在或添加成功或添加失败
 3    客户端请求删除用户    ['用户序列号']    删除成功或删除失败
 4    客户端请求修改密码    ['用户序列号', '修改前密码sha256', '修改后的密码sha256']    原密码错误或修改成功或修改失败
 5    客户端请求增加项目    ['用户序列号', 'url', '网站用户名', '网站密码']    添加成功或添加失败
 6    客户端请求删除项目    ['用户序列号', 'url', '网站用户名']    删除成功或删除失败
 7    客户端请求修改项目    [['用户序列号', 'url', '网站用户名', '网站密码'], ['修改后url', '修改后用户名', '修改后密码']]
'''


def message_handle(signal: int, content: list):
    # 客户端请求登录
    if signal == 1:
        db = userTable.select(None, content[0])
        if len(db) == 0:
            return 'UserNotExists'
        else:
            if db[2] == content[1]:
                # 此处将登陆成功信息及数据库内容放入list中再返回
                return 'LoginSuccess'
            elif not db[2] == content[1]:
                return 'PasswordIncorrect'

    # 客户端请求增加用户
    elif signal == 2:
        result = userTable.insert(content[0], content[1])
        if result == 'UserExists':
            return result
        else:
            if result:
                return 'InsertSuccess'
            elif not result:
                return 'InsertFail'

    # 客户端请求删除用户
    elif signal == 3:
        result = userTable.delete(content[0]) and detailTable.delete(content[0])
        if result:
            return 'DeleteSuccess'
        elif not result:
            return 'DeleteFail'

    # 客户端请求修改密码
    elif signal == 4:
        original_password = userTable.select(content[0], None)
        if original_password[2] == content[1]:
            result = userTable.update(content[0], None, content[2])
            if result == 'NothingToChange':
                return result
            else:
                if result:
                    return 'UpdateSuccess'
                elif not result:
                    return 'UpdateFail'
        else:
            return 'OriginalPasswordIncorrect'

    # 客户端请求增加项目
    elif signal == 5:
        result = detailTable.insert(content[0], content[1], content[2], content[3])
        if result:
            return 'InsertSuccess'
        elif not result:
            return 'InsertFail'

    # 客户端请求删除项目
    elif signal == 6:
        result = detailTable.delete(content[0], content[1], content[2])
        if result == 'NothingToDelete':
            return result
        else:
            if result:
                return 'DeleteSuccess'
            elif not result:
                return 'DeleteFail'

    # 客户端请求修改项目
    elif signal == 7:
        result = detailTable.update(content[0][0], content[0][1], content[0][2], content[0][3], content[1][0],
                                    content[1][1], content[1][2])
        if result == 'NothingToChange':
            return result
        else:
            if result:
                return 'UpdateSuccess'
            elif not result:
                return 'UpdateFail'
