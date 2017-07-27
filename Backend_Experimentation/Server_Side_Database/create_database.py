"""
Created on Fri Jul 28 11:22:34 2017
@author: Lysenthia
"""

def database_creation():
    """ Creates the initial database """
    import sqlite3
    DB_NAME = 'cloud_storage.db'
    DB_DIRECTORY = '/server_side_storage'
    db = sqlite3.connect('{}{}'.format(DB_DIRECTORY, DB_NAME))
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE user_ids
         (row_id INTEGER PRIMARY KEY, uid TEXT, user_table_name TEXT)''')
    #Each user will have their own table in the database
    db.commit()
    db.close()
    
