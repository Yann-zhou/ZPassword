from os import getcwd
import sqlite3
from ZSocketClient import socket_send
from secret_shamir import shamir_exec

from ast import literal_eval

def create():
    conn = sqlite3.connect(getcwd() + '/MyPass.db')
    c_create = conn.cursor()
    c_select = conn.cursor()
    cursor = c_select.execute('SELECT * FROM user')
    num_of_table = 0
    for row in cursor:
        try:
            sql_sentence = '''
                    CREATE TABLE detail''' + str(row[0]) + ''' (
                        id       INTEGER PRIMARY KEY ASC AUTOINCREMENT,
                        domain   TEXT,
                        user     TEXT,
                        password TEXT
                    );'''
            c_create.execute(sql_sentence)
            socket_send(sql_sentence)
            conn.commit()
            num_of_table += 1
        except sqlite3.OperationalError:
            pass
    conn.close()
    print(str(num_of_table) + ' of tables have been created.')


def insert(userid: str, domain: str, user: str, password: str):
    try:
        conn = sqlite3.connect(getcwd() + '/MyPass.db')
        c = conn.cursor()
        pass_list = shamir_exec.create('2of2', 0, str(password), 128)
        sql_sentence_local = 'INSERT INTO detail' + userid + ' (domain, user, password) VALUES ("' + domain + '", "' + user + '", "' + pass_list[0] + '");'
        sql_sentence_remote = 'INSERT INTO detail' + userid + ' (domain, user, password) VALUES ("' + domain + '", "' + user + '", "' + pass_list[1] + '");'
        c.execute(sql_sentence_local)
        socket_send(sql_sentence_remote)
        conn.commit()
        conn.close()
        return True
    except:
        return False


def select(userid: str):
    try:
        conn = sqlite3.connect(getcwd() + '/MyPass.db')
        c = conn.cursor()
        sql_sentence = 'SELECT * FROM detail' + userid
        cursor = c.execute(sql_sentence)
        socket_return = literal_eval(socket_send(sql_sentence).decode())
        print(socket_return)
        result = []
        print()
        i = 0
        for row in cursor:
            result.append([row[0], row[1], row[2], shamir_exec.recover([row[3], socket_return[i]])])
            i += 1
        conn.close()
        return result
    except:
        return 'UserHaveNoData'


def update(userid: str, original_domain: str, original_user: str, original_password: str, domain: str, user: str, password: str):
    try:
        conn = sqlite3.connect(getcwd() + '/MyPass.db')
        c = conn.cursor()
        pass_list = shamir_exec.create('2of2', 0, password, 128)
        sql_sentence_local = 'UPDATE detail'+userid+' SET domain=\''+domain+'\', user=\''+user+'\', password=\''+pass_list[0]+'\' WHERE domain=\''+original_domain+'\' AND user=\''+original_user+'\''
        sql_sentence_remote = 'UPDATE detail'+userid+' SET domain=\''+domain+'\', user=\''+user+'\', password=\''+pass_list[1]+'\' WHERE domain=\''+original_domain+'\' AND user=\''+original_user+'\''
        c.execute(sql_sentence_local)
        socket_send(sql_sentence_remote)
        conn.commit()
        if conn.total_changes > 0:
            conn.close()
            return True
        else:
            conn.close()
            return 'NothingToChange'
    except:
        return False


def delete(userid: str, domain: str = None, user: str = None):
    try:
        conn = sqlite3.connect(getcwd() + '/MyPass.db')
        c = conn.cursor()
        if domain is not None or user is not None:
            sql_sentence = 'DELETE FROM detail' + userid + ' WHERE domain=\'' + domain + '\' AND user=\'' + user + '\''
        else:
            sql_sentence = 'DROP TABLE detail'+userid
        c.execute(sql_sentence)
        socket_send(sql_sentence)
        conn.commit()
        if conn.total_changes > 0:
            return True
        else:
            return 'NothingToDelete'
        conn.close()
    except:
        return False
