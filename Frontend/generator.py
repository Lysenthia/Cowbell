class Song:
        
    #   REMEMBER TO ADD NOTE LINKING TO JSON

    def __init__(self, notes_to_play='C4C4C5C5B4G4A4B4C5C4C4A4A4G4G4G4G4', note_linking='dummy', author_name='Anon', outfile_name=None, cloud_db_pos=None):
        """ Constructs the song object """
        import datetime
        self.cloud_db_pos = cloud_db_pos
        self.CROSSFADE_LENGTH = 50
        self.UNIT_LENGTH = 2
        self.notes_to_play = notes_to_play
        self.creation_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        self.DB_DIRECTORY = 'database_outfiles/'
        self.WAV_DIRECTORY = 'wav_outfiles/'
        if note_linking == 'dummy':
            self.linked_notes = "0" * int((len(notes_to_play) / 2))
        else:
            self.linked_notes = note_linking
        if outfile_name == None:
            self.outfile_name = "{}music{}".format(self.WAV_DIRECTORY,self.creation_date)
        else:
            self.outfile_name = "{}{}".format(self.WAV_DIRECTORY,outfile_name)
        self.database_name = "music{}.cowbell".format(self.creation_date)
        self.outfile = str('{}'.format(self.outfile_name))
        self.author_name = author_name
        
    def make_wav(self, fileformat="wav"):
        """ Makes the song from notes_to_play"""
        from pydub import AudioSegment
        outfile_name = "{}.{}".format(self.outfile, fileformat)
        print(outfile_name)
        self.generated_notes = []
        if '1' in self.linked_notes:
            notes = self.linked_note_parser()
            infiles = []
            for note in notes:
                if isinstance(note, list):
                    note_length = len(note)
                    self.gen_note(note[0], note_length)
                    infiles.append('gened_notes/{}{}.wav'.format(note[0], note_length))
                    self.generated_notes.append('gened_notes/{}{}.wav'.format(note[0], note_length))
                else:
                    infiles.append('sound_array/{}.wav'.format(note))
        else:
            notes = [self.notes_to_play[i:i+self.UNIT_LENGTH] for i in range(0, len(self.notes_to_play), self.UNIT_LENGTH)]
            infiles = ['sound_array/{}.wav'.format(x) for x in notes]
        combinedAudio = AudioSegment.from_wav(infiles[0])
        infiles.pop(0)
        for infile in infiles:
            combinedAudio = combinedAudio.append(AudioSegment.from_wav(infile), crossfade=self.CROSSFADE_LENGTH)
        combinedAudio.export(outfile_name, format=fileformat, tags={'artist': self.author_name})
        self.garbage_gen_notes()
        return outfile_name
    
    def garbage(self, fileformat):
        """ Deletes the file (Hopefully this will be automated one day) """
        import os
        if fileformat == "cowbell":
            os.remove("{}{}".format(self.DB_DIRECTORY, self.database_name))    
        else:
            os.remove("{}{}".format(self.WAV_DIRECTORY, self.outfile))
        
    def garbage_gen_notes(self):
        """ Removes any notes made during son compilation """
        import os
        for file in set(self.generated_notes):
            os.remove(file)
        
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
        
    def linked_note_parser(self):
        """ Parses a song with linked notes """
        linked_notes = list(self.linked_notes)
        note_list = [self.notes_to_play[i:i+self.UNIT_LENGTH] for i in range(0, len(self.notes_to_play), self.UNIT_LENGTH)]
        linked_notes_dup = linked_notes
        list_with_groups = []
        note_index = 0
        cur = linked_notes_dup[0]
        while len(linked_notes_dup) > 0:
            if cur == '1' and note_list[note_index] == note_list[note_index + 1]:
                group = [note_list[note_index]]
                while cur == '1' and note_list[note_index] == note_list[note_index + 1]:
                    group.append(note_list[note_index])
                    linked_notes_dup.pop(0)
                    if len(linked_notes_dup) == 0:
                        break
                    note_index += 1
                    cur = linked_notes_dup[0]
                list_with_groups.append(group)
            else:
                list_with_groups.append(note_list[note_index])
            if len(linked_notes_dup) == 0:
                break
            note_index += 1
            linked_notes_dup.pop(0)
            cur = linked_notes_dup[0]
        return list_with_groups

    def gen_note(self, note, duration):
        import math
        import wave
        import struct
        note_list = [('A0', 27.50),('B0', 30.87),('C0', 16.35),('D0', 18.35),('E0', 20.60),('F0', 21.83),('G0', 24.50),
             ('A1', 55.00),('B1', 61.74	),('C1', 32.70),('D1', 36.71),('E1', 41.20),('F1', 43.65),('G1', 49.00),
             ('A2', 110.00),('B2', 123.47),('C2', 65.41),('D2', 73.42),('E2', 82.41),('F2', 87.31),('G2', 98.00),
             ('A3', 220.00),('B3', 246.94),('C3', 130.81,),('D3', 146.83),('E3', 164.81),('F3', 174.61),('G3', 196.00),
             ('A4', 440.00),('B4', 493.88),('C4', 261.63),('D4', 293.66),('E4', 329.63),('F4', 349.23),('G4', 392.00),
             ('A5', 880.00),('B5', 987.77),('C5', 523.25),('D5', 587.33),('E5', 659.25),('F5', 698.46),('G5', 783.99),
             ('A6', 1760.00),('B6', 1975.53),('C6', 1046.50),('D6', 1174.66),('E6', 1318.51),('F6', 1396.91),('G6', 1567.98),
             ('A7', 3520.00),('B7', 3951.07),('C7', 2093.00),('D7', 2349.32),('E7', 2637.02),('F7', 2793.83),('G7', 3135.96),
             ('A8',7040.00),('B8', 7902.13),('C8', 4186.01),('D8', 4698.63),('E8', 5274.04),('F8', 5587.65),('G8', 6271.93)]
        note_dic = dict(note_list)
        frequency = note_dic[note]
        sampleRate = 44100.0
        SAMPLE_LEN = sampleRate * duration * 0.5
        noise_output = wave.open('gened_notes/{}{}.wav'.format(note,duration), 'w')
        noise_output.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))
        sounds = []
        for i in range(0, int(SAMPLE_LEN)):
            packed_value = struct.pack('<h', int(32767.0*math.cos(frequency*math.pi*float(i)/float(sampleRate))))
            sounds.append(packed_value)
        sounds_str = b''.join(sounds)
        noise_output.writeframes(sounds_str)
        noise_output.close()