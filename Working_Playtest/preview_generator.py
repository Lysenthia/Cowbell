class Preview:
        
    def __init__(self, notes_to_play='C4C4C5C5B4G4A4B4C5C4C4A4A4G4G4G4G4'):
        """ Constructs the song object """
        import datetime
        self.CROSSFADE_LENGTH = 50
        self.UNIT_LENGTH = 2
        self.notes_to_play = notes_to_play
        self.creation_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        self.WAV_DIRECTORY = 'public/static/song_previews/'
        self.outfile_name = "{}music{}.wav".format(self.WAV_DIRECTORY,self.creation_date)
        self.outfile = str('{}'.format(self.outfile_name))
        
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
        """ Deletes the preview after playing """
        import os
        os.remove("{}{}".format(self.WAV_DIRECTORY, self.outfile))
