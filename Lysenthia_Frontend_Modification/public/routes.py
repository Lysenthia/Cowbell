from flask import g
from flask import render_template
from flask import request
from flask import redirect
from flask import send_from_directory
from flask import flash
from public import website
from generator import Song
import os


#HOMEPAGE/NOTE AMOUNT ENTER
@website.route('/', methods=['GET', 'POST'])
def index():
	error = None
	if request.method == 'POST':
		noteamt = request.form.get('notes')
		if noteamt == "" or noteamt == "0":
			error = "Please enter a non-zero number."
			return render_template('index.html', error=error)
		else:
			noteamt = abs(int(noteamt))
			return redirect('/synth/{}'.format(str(noteamt)))
	else:
		return render_template('index.html', error=error)



#SYNTH PAGE
@website.route('/synth/<notes>')#, methods=['GET', 'POST'])
def synth(notes = None):
	#if request.method == 'POST':
	#	print("Sup")
	#else:
	return render_template('synth.html', notes=notes)


#DISPLAYS WHEN WAV EXPORTED
@website.route('/exported', methods=['GET', 'POST'])
def exported():
	#Dictionary of the slider values that correspond to the note values
	noteDict = {0:"C4", 1:"D4", 2:"E4", 3:"F4", 4:"G4", 5:"A4", 6:"B4", 7:"C5"}
	sliderValues = {}
	noteValues = []
	sliderKeys = []
	#Get the submitted slider values from the previous page
	rawSliderValues = request.values if request.method == "GET" else request.values

	#Extract the data from rawSliderValues and add it to sliderValues (Also get rid of "exporttowav")
	for key in rawSliderValues:
		if key != "exporttowav":
			temp_key = int(key[6:])
			sliderValues[temp_key] = rawSliderValues[key]

	#Create a sorted list of the keys from slider values
	sliderKeys = sorted(sliderValues)
	print(sliderKeys)
	###  Get each note value from the noteDict in order using the sorted sliderKeys 
	###  list to call values from sliderValues in the original order
	for item in sliderKeys:
		noteValues.append(noteDict[int(sliderValues[item])])

	#Convert noteValues to string
	sNoteValues = ''.join(noteValues)
	#Create WAV file from the string version of noteValues
	song = Song(sNoteValues)
	wavFileName = song.make_wav()
	#Return the exported page and attach the filename of the exported WAV file
	return render_template('exported.html', wavFileName = wavFileName)

@website.route('/return-file/<wavfilename>')
def return_file(wavfilename):
	directory = os.getcwd()
	return send_from_directory(directory, wavfilename, attachment_filename=wavfilename, as_attachment=True, mimetype='audio/wav')
