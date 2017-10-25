# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 11:04:32 2017

@author: Lysenthia
"""
class CowbellError(Exception):
    """ Invalid Cowbell file """
    
def validate_cowbell_file(filename):
    import sqlite3
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("""select count(*) from sqlite_master where type='table' and name='song_data'""")
    db.commit()
    cursor.close()
    db.close()

