from os import getcwd
import sqlite3


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
    except sqlite3.IntegrityError:
        print('UNIQUE constraint failed: user.user')


def select(user: str):
    conn = sqlite3.connect(getcwd() + '/MyPass.db')
    c = conn.cursor()
    cursor = c.execute('SELECT * FROM user WHERE user=\'' + user + '\'')
    db = cursor.fetchall()
    conn.close()
    return db


def update(userid: str, user: str = None, password: str = None):
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
    print('Total changes is:', conn.total_changes)
    conn.close()


def delete(userid: str):
    conn = sqlite3.connect(getcwd() + '/MyPass.db')
    c = conn.cursor()
    execute_sentence = 'DELETE FROM user WHERE id=' + userid
    c.execute(execute_sentence)
    conn.commit()
    conn.close()
