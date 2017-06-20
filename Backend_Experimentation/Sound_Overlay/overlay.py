from pydub import AudioSegment
sound1 = AudioSegment.from_wav("wav1.wav")
sound2 = AudioSegment.from_wav("wav2.wav")
output = sound1.overlay(sound2)
output.export("mixed_sounds.wav", format="wav")
