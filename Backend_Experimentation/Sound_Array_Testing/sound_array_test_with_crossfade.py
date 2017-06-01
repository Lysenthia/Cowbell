import wave
import datetime
from pydub import AudioSegment

CROSSFADE_LENGTH = 50
UNIT_LENGTH = 2

def make_wave(notes_to_play='C4C4C5C5B4G4A4B4C5C4C4A4A4G4G4G4G4', outfile_name=None):
    """ Makes the song from notes_to_play"""
    creation_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    notes = [notes_to_play[i:i+UNIT_LENGTH] for i in range(0, len(notes_to_play), UNIT_LENGTH)]
    infiles = ['sound_array/{}.wav'.format(x) for x in notes]
    print(infiles)
    if name == None:
        outfile = "music{}.wav".format(creation_date)
    else:
        outfile = outfile_name
    parameters = (1, 2, 44100, 0, 'NONE', 'not compressed')
    combinedAudio = AudioSegment.from_wav(infiles[0])
    infiles.pop(0)
    for infile in infiles:
        combinedAudio = combinedAudio.append(AudioSegment.from_wav(infile), crossfade=CROSSFADE_LENGTH)
    combinedAudio.export(outfile, format="wav")
