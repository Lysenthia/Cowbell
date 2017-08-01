"""
Created on Fri Jul 28 11:22:34 2017
@author: Lysenthia
REMINDER: rework later so that DB_NAME and DB_DIRECTORY are passed to the functions
"""
class DropTablesError(Exception):
    """ Somebody tried to drop tables us """
    
def create_database():
    """ Creates the initial database """
    import sqlite3
    DB_NAME = 'cloud_storage.db'
    DB_DIRECTORY = 'server_side_storage/'
    db = sqlite3.connect('{}/{}'.format(DB_DIRECTORY, DB_NAME))
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE user_ids
         (row_id INTEGER PRIMARY KEY AUTOINCREMENT, uid TEXT, user_table_name TEXT)''')
    db.commit()
    cursor.close()
    db.close()
    
def add_user(uid):
    """ Creates a new table in the database containing a users projects """
    if "drop tables" in uid:
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    import sqlite3
    DB_NAME = 'cloud_storage.db'
    DB_DIRECTORY = 'server_side_storage/'
    db = sqlite3.connect('{}{}'.format(DB_DIRECTORY, DB_NAME))
    user_table_name = uid   #This might be changed later
    cursor = db.cursor()
    cursor.execute("INSERT INTO user_ids VALUES (NULL, ?,?)",(uid, user_table_name))
    variable_table_command = '''CREATE TABLE {} (row_id INTEGER PRIMARY KEY AUTOINCREMENT, song_notes TEXT, author_name TEXT, creation_date TEXT, project_name TEXT)'''.format(user_table_name)
    cursor.execute(variable_table_command)
    db.commit()
    cursor.close()
    db.close()

def add_project(uid, song_notes, author_name, creation_date, project_name):
    """ Adds the data for a project to a users table in the database """
    if any('drop tables' in var for var in [uid, song_notes, author_name, creation_date, project_name]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    import sqlite3
    DB_NAME = 'cloud_storage.db'
    DB_DIRECTORY = 'server_side_storage/'
    db = sqlite3.connect('{}{}'.format(DB_DIRECTORY, DB_NAME))
    cursor = db.cursor()
    cursor.execute("SELECT user_table_name FROM user_ids WHERE uid=?", (uid,))
    table_name = cursor.fetchall()
    table_name = table_name[0][0]
    print(table_name)
    variable_table_command = '''INSERT INTO {} VALUES (NULL, '{}','{}','{}','{}')'''.format(table_name, song_notes, author_name, creation_date, project_name)
    print(variable_table_command)
    cursor.execute(variable_table_command)
    db.commit()
    cursor.close()
    db.close()
    
def get_uids():
    """ Gets all uids and returns them as a list """
    import sqlite3, itertools
    DB_NAME = 'cloud_storage.db'
    DB_DIRECTORY = 'server_side_storage/'
    db = sqlite3.connect('{}{}'.format(DB_DIRECTORY, DB_NAME))
    cursor = db.cursor()
    cursor.execute("SELECT uid FROM user_ids")
    all_uids = cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()
    all_uids = list(itertools.chain(*all_uids))
    return all_uids