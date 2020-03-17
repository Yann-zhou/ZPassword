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
            print('table already exists')
    conn.close()
    print(str(num_of_table) + ' of tables have been created.')


def insert(userid: str, domain: str, user: str, password: str):
    conn = sqlite3.connect(getcwd() + '/MyPass.db')
    c = conn.cursor()
    c.execute('''
            INSERT INTO detail''' + userid + ''' (domain, user, password)
            VALUES (\'''' + domain + "\', \'" + user + "\', \'" + password + '''\');
    ''')
    conn.commit()
    conn.close()


def select(userid: str):
    conn = sqlite3.connect(getcwd() + '/MyPass.db')
    c = conn.cursor()
    cursor = c.execute('SELECT * FROM detail' + userid)
    for row in cursor:
        print(row)
    conn.close()


def update(userid: str, record_id: str, domain: str = None, user: str = None, password: str = None):
    conn = sqlite3.connect(getcwd() + '/MyPass.db')
    c = conn.cursor()
    execute_sentence = 'UPDATE detail' + record_id + ' SET '
    if domain is not None:
        execute_sentence += 'domain = \'' + domain + '\', '
    if user is not None:
        execute_sentence += 'user = \'' + user + '\', '
    if password is not None:
        execute_sentence += 'password = \'' + password + '\', '
    execute_sentence = execute_sentence[:-2]
    execute_sentence += ' WHERE id = ' + userid

    c.execute(execute_sentence)
    conn.commit()
    print('Total changes is:', conn.total_changes)
    conn.close()


def delete(userid: str, record_id: str = None):
    conn = sqlite3.connect(getcwd() + '/MyPass.db')
    c = conn.cursor()
    if record_id is not None:
        execute_sentence = 'DELETE FROM detail' + userid + ' WHERE id=\'' + record_id + '\''
    else:
        execute_sentence = 'DROP TABLE detail'+userid
    c.execute(execute_sentence)
    conn.commit()
    conn.close()