from os import getcwd
import sqlite3


def create():
    conn = sqlite3.connect(getcwd() + '/MyPass.db')
    c_create = conn.cursor()
    c_select = conn.cursor()
    cursor = c_select.execute('SELECT * FROM user')
    num_of_table = 0
    for row in cursor:
        try:
            c_create.execute('''
                    CREATE TABLE detail''' + str(row[0]) + ''' (
                        id       INTEGER PRIMARY KEY ASC AUTOINCREMENT,
                        domain   STRING,
                        user     STRING,
                        password STRING
                    );''')
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
        c.execute('''
                INSERT INTO detail''' + userid + ''' (domain, user, password)
                VALUES (\'''' + domain + "\', \'" + user + "\', \'" + password + '''\');
        ''')
        conn.commit()
        conn.close()
        return True
    except:
        return False


def select(userid: str):
    try:
        conn = sqlite3.connect(getcwd() + '/MyPass.db')
        c = conn.cursor()
        cursor = c.execute('SELECT * FROM detail' + userid)
        result = []
        for row in cursor:
            result.append([row[0], row[1], row[2], row[3]])
        conn.close()
        return result
    except:
        return 'UserHaveNoData'


def update(userid: str, original_domain: str, original_user: str, original_password: str, domain: str, user: str, password: str):
    try:
        conn = sqlite3.connect(getcwd() + '/MyPass.db')
        c = conn.cursor()
        execute_sentence = 'UPDATE detail'+userid+' SET domain=\''+domain+'\', user=\''+user+'\', password=\''+password+'\' WHERE domain=\''+original_domain+'\' AND user=\''+original_user+'\' AND password=\''+original_password+'\''
        c.execute(execute_sentence)
        conn.commit()
        # print('Total changes is:', conn.total_changes)
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
            execute_sentence = 'DELETE FROM detail' + userid + ' WHERE domain=\'' + domain + '\' AND user=\'' + user + '\''
        else:
            execute_sentence = 'DROP TABLE detail'+userid
        c.execute(execute_sentence)
        conn.commit()
        if conn.total_changes > 0:
            return True
        else:
            return 'NothingToDelete'
        conn.close()
    except:
        return False
