import sqlite3
INFILE = "saved_song.cowbell"
try:
    with sqlite3.connect(INFILE) as db:
        cursor.execute("select SongNotes from song_data")
        song_notes = cursor.fetchall()
        song_notes = "".join(map("".join, song_notes))
    print(song_notes)
except FileNotFoundError:
    print("Error 404 - File not found :-p")