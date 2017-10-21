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
    cursor.execute('''CREATE TABLE users(
        ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        UID TEXT, 
        author_name TEXT)''')

    cursor.execute('''CREATE TABLE songs(
        ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        song_notes TEXT, 
        creation_date TEXT, 
        project_name TEXT,
        user_ID INTEGER, 
        FOREIGN KEY(user_ID) REFERENCES users(ID)
        )''')
    db.commit()
    cursor.close()
    db.close()
    
def add_user(DB_NAME, DB_DIRECTORY, uid, author_name="Anon"):
    """ Creates a new table in the database containing a users projects """
    if any('drop tables' in var for var in [DB_NAME, DB_DIRECTORY, uid]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    db = sqlite3.connect('{}/{}'.format(DB_DIRECTORY, DB_NAME))
    cursor = db.cursor()
    cursor.execute("INSERT INTO users VALUES (NULL, ?,?)",(uid, author_name))
    db.commit()
    cursor.close()
    db.close()

def add_project(DB_NAME, DB_DIRECTORY, user_ID, song_notes, creation_date, project_name):
    """ Adds the data for a project to a users table in the database """
    if any('drop tables' in var for var in [DB_NAME, DB_DIRECTORY, user_ID, song_notes, creation_date, project_name]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    db = sqlite3.connect('{}/{}'.format(DB_DIRECTORY, DB_NAME))
    cursor = db.cursor()
    cursor.execute("INSERT INTO songs VALUES (NULL, ?,?,?,?)",(song_notes, creation_date, user_ID, project_name))
    db.commit()
    cursor.close()
    db.close()
    
def get_uids(DB_NAME, DB_DIRECTORY):
    """ Gets all uids and returns them as a list """
    import itertools
    if any('drop tables' in var for var in [DB_NAME, DB_DIRECTORY]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    db = sqlite3.connect('{}/{}'.format(DB_DIRECTORY, DB_NAME))
    cursor = db.cursor()
    cursor.execute("SELECT UID FROM users")
    all_uids = cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()
    all_uids = list(itertools.chain(*all_uids))
    return all_uids

def save_project(DB_NAME, DB_DIRECTORY, uid, song_ID, project_name, song_notes):
    """ Saves an already existing page to the database """
    if any('drop tables' in var for var in [DB_NAME, DB_DIRECTORY, uid]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    db = sqlite3.connect('{}/{}'.format(DB_DIRECTORY, DB_NAME))
    cursor = db.cursor()
    cursor.execute("SELECT ID FROM users WHERE UID=?",(uid,))
    user_ID = cursor.fetchall()
    user_ID = user_ID[0][0]
    cursor.execute("UPDATE songs SET song_notes = ?, project_name = ? WHERE user_ID=? AND ID=?",(song_notes, project_name, user_ID, song_ID,))
    db.commit()
    cursor.close()
    db.close()
    return True
    
def open_project(DB_NAME, DB_DIRECTORY, uid, song_ID):
    """ Opens a project for use """
    if any('drop tables' in var for var in [DB_NAME, DB_DIRECTORY, uid]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    db = sqlite3.connect('{}/{}'.format(DB_DIRECTORY, DB_NAME))
    cursor = db.cursor()
    cursor.execute("SELECT songs.ID, song_notes, author_name, creation_date, project_name FROM songs INNER JOIN users ON users.ID = songs.user_ID WHERE songs.ID=? AND UID=?",(song_ID, uid,))
    project_data = cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()
    return project_data

def list_projects(DB_NAME, DB_DIRECTORY, UID):
    """ Returns a list of tuple triplets of creation_date, project_name and song_ID for a users songs """
    if any('drop tables' in var for var in [DB_NAME, DB_DIRECTORY, UID]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    db = sqlite3.connect('{}/{}'.format(DB_DIRECTORY, DB_NAME))
    cursor = db.cursor()
    cursor.execute("SELECT ID FROM users WHERE UID=?",(UID,))
    user_ID = cursor.fetchall()
    user_ID = user_ID[0][0]
    cursor.execute("SELECT creation_date, project_name, ID FROM songs WHERE user_ID=?",(user_ID,))
    projects = cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()
    return projects

#print(open_project("cloud_save.db", "public/static/db", "thisismyuid", 1)[0][1])

#save_project("database.db", "server_side_storage", "thisistheuidomg12345", 3, "yser 1's cool project", "oldsongnotes")
