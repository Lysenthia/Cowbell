"""
Created on Fri Jul 28 11:22:34 2017
@author: Lysenthia and dr-ex
"""
import sqlite3
class DropTablesError(Exception):
    """ Somebody tried to drop tables us """
    
def create_database(DB_NAME, DB_DIRECTORY):
    """ Creates the initial database """
    db = sqlite3.connect('{}/{}'.format(DB_DIRECTORY, DB_NAME))
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE users
         (ID INTEGER PRIMARY KEY AUTOINCREMENT, uid TEXT, author_name TEXT)''')
    db.commit()
    cursor.close()
    db.close()
    
def add_user(DB_NAME, DB_DIRECTORY, uid):
    """ Creates a new table in the database containing a users projects """
    if any('drop tables' in var for var in [DB_NAME, DB_DIRECTORY, uid]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    db = sqlite3.connect('{}{}'.format(DB_DIRECTORY, DB_NAME))
    user_table_name = uid   #This might be changed later
    cursor = db.cursor()
    cursor.execute("INSERT INTO user_ids VALUES (NULL, ?,?)",(uid, user_table_name))
    variable_table_command = '''CREATE TABLE {} (row_id INTEGER PRIMARY KEY AUTOINCREMENT, song_notes TEXT, author_name TEXT, creation_date TEXT, project_name TEXT)'''.format(user_table_name)
    cursor.execute(variable_table_command)
    db.commit()
    cursor.close()
    db.close()

def add_project(DB_NAME, DB_DIRECTORY, uid, song_notes, author_name, creation_date, project_name):
    """ Adds the data for a project to a users table in the database """
    if any('drop tables' in var for var in [DB_NAME, DB_DIRECTORY, uid, song_notes, author_name, creation_date, project_name]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
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
    
def get_uids(DB_NAME, DB_DIRECTORY):
    """ Gets all uids and returns them as a list """
    import itertools
    if any('drop tables' in var for var in [DB_NAME, DB_DIRECTORY]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    db = sqlite3.connect('{}{}'.format(DB_DIRECTORY, DB_NAME))
    cursor = db.cursor()
    cursor.execute("SELECT uid FROM user_ids")
    all_uids = cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()
    all_uids = list(itertools.chain(*all_uids))
    return all_uids

def save_project(DB_NAME, DB_DIRECTORY, uid, song_notes, author_name, creation_date, project_name):
    """ Saves an already existing page to the database """
    
def open_project(DB_NAME, DB_DIRECTORY, uid, project_to_open):
    """ Opens a project for use """
    import itertools
    if any('drop tables' in var for var in [DB_NAME, DB_DIRECTORY, uid, str(project_to_open)]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    db = sqlite3.connect('{}{}'.format(DB_DIRECTORY, DB_NAME))
    cursor = db.cursor()
    cursor.execute("SELECT user_table_name FROM user_ids WHERE uid=?", (uid,))
    table_name = cursor.fetchall()
    table_name = table_name[0][0]
    variable_table_command = "SELECT * FROM {} WHERE row_id={}".format(table_name, project_to_open)
    cursor.execute(variable_table_command)
    project_data = cursor.fetchall()
    project_data = list(itertools.chain(*project_data))
    db.commit()
    cursor.close()
    db.close()
    return project_data