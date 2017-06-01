import sqlite3, itertools
INFILE = "saved_song.cowbell"
with sqlite3.connect(INFILE) as db:
    cursor = db.cursor()                                                                                                                        #Sets up cursor
    cursor.execute("select SongNotes from song_data")
    song_notes = str(cursor.fetchall())
    print(song_notes)