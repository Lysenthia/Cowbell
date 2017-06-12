class Song:
        
    def __init__(self, notes_to_play='C4C4C5C5B4G4A4B4C5C4C4A4A4G4G4G4G4', author_name='Anon', outfile_name=None):
        """ Constructs the song object """
        import datetime
        self.CROSSFADE_LENGTH = 50
        self.UNIT_LENGTH = 2
        self.notes_to_play = notes_to_play
        self.creation_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        if outfile_name == None:
            self.outfile = "music{}.wav".format(self.creation_date)
        else:
            self.outfile = "{}.wav".format(outfile_name)
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
        combinedAudio.export(self.outfile, format="wav")
        return self.outfile
    
    def garbage(self):
        """ Deletes the file (Hopefully this will be automated one day) """
        import os
        os.remove(self.outfile)
        
    def write_to_database(self):
        """ Writes the song to an SQLite3 Database """
        import sqlite3
        database_name = "music{}.cowbell".format(self.creation_date)
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE song_data
             (row_id INTEGER PRIMARY KEY, song_notes TEXT, author_name TEXT, creation_date TEXT, project_name TEXT)''')
        cursor.execute("INSERT INTO song_notes VALUES ('2006-01-05',{0},{1},{2},{3})".format(self.notes_to_play, self.author_name, self.creation_date))