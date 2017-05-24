import wave
UNIT_LENGTH = 2

notes_to_play = 'C4C4C5C5B4G4A4B4C5C4C4A4A4G4G4G4G4'
notes = [notes_to_play[i:i+UNIT_LENGTH] for i in range(0, len(notes_to_play), UNIT_LENGTH)]
infiles = ['sound_array/{}.wav'.format(x) for x in notes]
print(infiles)
outfile = "music.wav"
parameters = (1, 2, 44100, 0, 'NONE', 'not compressed')
data= []
for infile in infiles:
    w = wave.open(infile, 'rb')
    data.append(w.readframes(w.getnframes()))
    w.close()

output = wave.open(outfile, 'wb')
output.setparams(parameters)
for note in data:
    output.writeframes(note)
output.close()
