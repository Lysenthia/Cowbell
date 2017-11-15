# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 11:04:32 2017

@author: Lysenthia
"""
def valid_cowbell_file(filename):
    COLUMN_NAMES = ["row_id","song_notes","author_name","creation_date","project_name"]
    COLUMN_TYPES = ["INTEGER","TEXT","TEXT","TEXT","TEXT"]
    import sqlite3, os
    if not os.path.isfile(filename):
        return False, "File doesn't exist (Somehow)"
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    try:
        cursor.execute("""select count(*) from sqlite_master where type='table' and name='song_data'""")
    except sqlite3.DatabaseError:
        return False,  "Not a valid SQLite3 database"
    table_check = cursor.fetchone()
    if not table_check[0]:
        return False, "song_data table does not exist"
    cursor.execute("""PRAGMA table_info(song_data)""")
    columns = cursor.fetchall()
    index = 0
    for column in columns:
        if not (COLUMN_TYPES[index] == column[2] and COLUMN_NAMES[index] == column[1]):
            return False, "Invalid column layout"
        index += 1
    cursor.execute("""SELECT * FROM song_data WHERE row_id=1""")
    data = cursor.fetchone()
    print(data)
    if None or "" in data:
        return False, "Data contains None or empty value(s)"
    db.commit()
    cursor.close()
    db.close()
    return True, "File Valid"

