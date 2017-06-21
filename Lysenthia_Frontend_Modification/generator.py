class Song:
        
    def __init__(self, notes_to_play='C4C4C5C5B4G4A4B4C5C4C4A4A4G4G4G4G4', author_name='Anon', outfile_name=None):
        """ Constructs the song object """
        import datetime
        self.CROSSFADE_LENGTH = 50
        self.UNIT_LENGTH = 2
        self.notes_to_play = notes_to_play
        self.creation_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        self.DB_DIRECTORY = 'database_outfiles/'
        self.WAV_DIRECTORY = 'wav_outfiles/'
        if outfile_name == None:
            self.outfile_name = "{}music{}.wav".format(self.WAV_DIRECTORY,self.creation_date)
        else:
            self.outfile_name = "{}{}.wav".format(self.WAV_DIRECTORY,outfile_name)
        self.database_name = "music{}.cowbell".format(self.creation_date)
        self.outfile = str('{}'.format(self.outfile_name))
        self.author_name = author_name
        
    def make_wav(self):
        """ Makes the song from notes_to_play"""
        from pydub import AudioSegment
        notes = [self.notes_to_play[i:i+self.UNIT_LENGTH] for i in range(0, len(self.notes_to_play), self.UNIT_LENGTH)]
        infiles = ['sound_array/{}.wav'.format(x) for x in notes]
        combinedAudio = AudioSegment.from_wav(infiles[0])
        infiles.pop(0)
        for infile in infiles:
            combinedAudio = combinedAudio.append(AudioSegment.from_wav(infile), crossfade=self.CROSSFADE_LENGTH)
        combinedAudio.export(self.outfile, format="wav", tags={'artist': self.author_name})
        return self.outfile
    
    def garbage(self):
        """ Deletes the file (Hopefully this will be automated one day) """
        import os
        os.remove("{}{}".format(self.WAV_DIRECTORY, self.outfile))
        os.remove("{}{}".format(self.DB_DIRECTORY, self.database_name))
        
    def write_to_database(self):
        """ Writes the song to an SQLite3 Database """
        import sqlite3
        db = sqlite3.connect('{}{}'.format(self.DB_DIRECTORY,self.database_name))
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE song_data
             (row_id INTEGER PRIMARY KEY, song_notes TEXT, author_name TEXT, creation_date TEXT, project_name TEXT)''')
        cursor.execute("INSERT INTO song_data VALUES (1,?,?,?,?)",(self.notes_to_play, self.author_name, self.creation_date, self.outfile_name))
        db.commit()
        db.close()
        return self.database_name

    def read_from_database(self, database_name):
        """ This might need to be moved to somewhere else. (As the song has already been constructed) """
        import os
        import sqlite3
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
        cursor.execute("select song_notes from song_data")
        self.notes_to_play = cursor.fetchall()
        self.notes_to_play = "".join(map("".join, self.notes_to_play))
        cursor.execute("select author_name from song_data")
        self.author_name = cursor.fetchall()
        self.author_name = "".join(map("".join, self.author_name))
        cursor.execute("select creation_date from song_data")
        self.creation_date = cursor.fetchall()
        self.creation_date = "".join(map("".join, self.creation_date))
        cursor.execute("select project_name from song_data")
        self.outfile_name = cursor.fetchall()
        self.outfile_name = "".join(map("".join, self.outfile_name))
        self.outfile = str(self.outfile_name)
        db.close()
        os.remove(database_name)
        
