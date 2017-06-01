import math
import wave
import struct

note_list = ['a','b','c','d','e','f','g','2']
note_frequency = [220.00,246.94,261.63,293.66,329.63,349.23,392.00, 'empty']
notes_to_play = list('eefggfedccdeedd2')
sampleRate = 44100.0
duration = int(input("Enter Duration"))
SAMPLE_LEN = sampleRate * duration
frequency = note_frequency[note_list.index('a')]

frequenies_to_play = []
for x in notes_to_play:
        frequenies_to_play.append(note_frequency[note_list.index(x)])
print(frequenies_to_play)

noise_output = wave.open('sound.wav', 'w')
noise_output.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))
sounds = []
for freq in frequenies_to_play:       
        if freq == 'empty':
                sounds.pop()
                freq_to_use = frequenies_to_play[frequenies_to_play.index(freq) - 1]
                print(freq_to_use)
                for i in range(0, int(SAMPLE_LEN/len(frequenies_to_play))):
                        packed_value = struct.pack('<h', int(32767.0*math.cos(freq_to_use*math.pi*float(i)/float(sampleRate))))
                        sounds.append(packed_value)
        else:
                for i in range(0, int(SAMPLE_LEN/len(frequenies_to_play))):
                        packed_value = struct.pack('<h', int(32767.0*math.cos(freq*math.pi*float(i)/float(sampleRate))))
                        sounds.append(packed_value)
                #packed_value = struct.pack('<h', 0)
                #sounds.append(packed_value)

sounds_str = b''.join(sounds)
noise_output.writeframes(sounds_str)
noise_output.close()
