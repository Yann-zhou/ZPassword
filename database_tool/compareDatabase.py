from database_tool import userTable


def compare_password(user: str, password: str):
    try:
        user_list = userTable.select(user)[0]
        if user_list[2] == password:
            return True
        else:
            return False
    except:
        return 'UserNotExists'