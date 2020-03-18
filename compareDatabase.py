from databaseTool import userTable
from databaseTool import detailTable


def compare_password(user: str, password: str):
    user_list = userTable.select(user)[0]
    if user_list[2] == password:
        return True
    else:
        return False
