from pydub import AudioSegment
from pydub.playback import play

def playback_wav(notes_to_play='C4C4C5C5B4G4A4B4C5C4C4A4A4G4G4G4G4'):
    """ Makes the song from notes_to_play"""
    CROSSFADE_LENGTH = 50
    UNIT_LENGTH = 2
    notes = [notes_to_play[i:i+UNIT_LENGTH] for i in range(0, len(notes_to_play), UNIT_LENGTH)]
    infiles = ['sound_array/{}.wav'.format(x) for x in notes]
    combinedAudio = AudioSegment.from_wav(infiles[0])
    infiles.pop(0)
    for infile in infiles:
        combinedAudio = combinedAudio.append(AudioSegment.from_wav(infile), crossfade=CROSSFADE_LENGTH)
    return combinedAudio

song = playback_wav()
play(song)



