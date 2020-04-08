from os import getcwd
import sqlite3

from database_tool import detailTable


def create():
    try:
        conn = sqlite3.connect(getcwd() + '/MyPass.db')
        c = conn.cursor()
        c.execute('''
                    CREATE TABLE user (
                        id       INTEGER    PRIMARY KEY ASC AUTOINCREMENT,
                        user     CHAR (50)  UNIQUE ON CONFLICT ROLLBACK,
                        password CHAR (100) 
                    );''')

        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        print('table already exists')


def insert(user: str, password: str):
    try:
        conn = sqlite3.connect(getcwd() + '/MyPass.db')
        c = conn.cursor()
        c.execute('''
                INSERT INTO user (user, password)
                VALUES (\'''' + user + "\', \'" + password + '''\')
        ''')
        conn.commit()
        conn.close()
        detailTable.create()
        return True
    except sqlite3.IntegrityError:
        return 'UserExists'
    except:
        return False


def select(userid: str = None, user: str = None):
    conn = sqlite3.connect(getcwd() + '/MyPass.db')
    c = conn.cursor()
    if userid is None:
        print('SELECT * FROM user WHERE user=\'' + user + '\'')
        cursor = c.execute('SELECT * FROM user WHERE user=\'' + user + '\'')
    elif user is None:
        cursor = c.execute('SELECT * FROM user WHERE id=\'' + userid + '\'')
    db = cursor.fetchall()
    conn.close()
    try:
        return [db[0][0], db[0][1], db[0][2]]
    except:
        return None


def update(userid: str, user: str = None, password: str = None):
    try:
        conn = sqlite3.connect(getcwd() + '/MyPass.db')
        c = conn.cursor()
        execute_sentence = 'UPDATE user SET '
        if user is not None:
            execute_sentence += 'user = \'' + user + '\', '
        if password is not None:
            execute_sentence += 'password = \'' + password + '\', '
        execute_sentence = execute_sentence[:-2]
        execute_sentence += 'WHERE id = ' + userid
        c.execute(execute_sentence)
        conn.commit()
        #print('Total changes is:', conn.total_changes)
        if conn.total_changes:
            return True
        else:
            return 'NothingToChange'
        conn.close()
    except:
        return False


def delete(user: str):
    try:
        conn = sqlite3.connect(getcwd() + '/MyPass.db')
        c = conn.cursor()
        execute_sentence = 'DELETE FROM user WHERE user=' + user
        c.execute(execute_sentence)
        conn.commit()
        conn.close()
        return True
    except:
        return False