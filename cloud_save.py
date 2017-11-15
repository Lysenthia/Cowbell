"""
Created on Fri Jul 28 11:22:34 2017
@author: Lysenthia and dr-ex
"""
import sqlite3
class DropTablesError(Exception):
    """ Somebody tried to drop tables us """
    
def create_database(db, cursor):
    """ Creates the initial database """
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
    
def add_user(db, cursor, uid, author_name="Anon"):
    """ Creates a new table in the database containing a users projects """
    if any('drop tables' in var for var in [uid]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    cursor.execute("INSERT INTO users VALUES (NULL, ?,?)",(uid, author_name))
    db.commit()

def add_project(db, cursor, user_ID, song_notes, creation_date, project_name):
    """ Adds the data for a project to a users table in the database """
    if any('drop tables' in var for var in [str(user_ID), song_notes, creation_date, project_name]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    cursor.execute("INSERT INTO songs VALUES (NULL, ?,?,?,?)",(song_notes, creation_date, project_name, user_ID))
    db.commit()
    return True
    
def get_uids(db, cursor):
    """ Gets all uids and returns them as a list """
    import itertools
    cursor.execute("SELECT UID FROM users")
    all_uids = cursor.fetchall()
    db.commit()
    all_uids = list(itertools.chain(*all_uids))
    return all_uids

def save_project(db, cursor, uid, song_ID, project_name, song_notes):
    """ Saves an already existing page to the database """
    if any('drop tables' in var for var in [uid]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    cursor.execute("SELECT ID FROM users WHERE UID=?",(uid,))
    user_ID = cursor.fetchall()
    user_ID = user_ID[0][0]
    cursor.execute("UPDATE songs SET song_notes = ?, project_name = ? WHERE user_ID=? AND ID=?",(song_notes, project_name, user_ID, song_ID,))
    db.commit()
    return True
    
def open_project(db, cursor, uid, song_ID):
    """ Opens a project for use """
    if any('drop tables' in var for var in [uid]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    cursor.execute("SELECT songs.ID, song_notes, author_name, creation_date, project_name FROM songs INNER JOIN users ON users.ID = songs.user_ID WHERE songs.ID=? AND UID=?",(song_ID, uid,))
    project_data = cursor.fetchall()
    db.commit()
    return project_data

def list_projects(db, cursor, UID):
    """ Returns a list of tuple triplets of creation_date, project_name and song_ID for a users songs """
    if any('drop tables' in var for var in [UID]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    cursor.execute("SELECT ID FROM users WHERE UID=?",(UID,))
    user_ID = cursor.fetchall()
    user_ID = user_ID[0][0]
    cursor.execute("SELECT creation_date, project_name, ID FROM songs WHERE user_ID=?",(user_ID,))
    projects = cursor.fetchall()
    db.commit()
    return projects

def get_user_data(db, cursor, UID):
    """ Gets the users data and returns it as a list """
    if any('drop tables' in var for var in [UID]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    cursor.execute("SELECT * FROM users WHERE UID=?",(UID,))
    user_data = cursor.fetchone()
    db.commit()
    return user_data

def change_user_name(db, cursor, UID, name):
    """ Gets the users data and returns it as a list """
    if any('drop tables' in var for var in [UID, name]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    cursor.execute("UPDATE users SET author_name=? WHERE UID=?",(name,UID,))
    db.commit()
    
def change_song_name(db, cursor, song_id, song_name):
    """ Changes the name of a song  """
    if any('drop tables' in var for var in [song_id, song_name]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    cursor.execute("UPDATE songs SET project_name=? WHERE ID=?",(song_name,song_id,))
    db.commit()
    
def close_database(db, cursor):
    cursor.close()
    db.close()

def open_database(DB_NAME, DB_DIRECTORY):
    if any('drop tables' in var for var in [DB_NAME, DB_DIRECTORY]):
        raise DropTablesError("Drop Tables command detected in input commands - Print Error Message")
    db = sqlite3.connect('{}/{}'.format(DB_DIRECTORY, DB_NAME))
    cursor = db.cursor()
    return db, cursor
