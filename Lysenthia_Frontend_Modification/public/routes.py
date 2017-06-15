from flask import g
from flask import render_template
from flask import request
from flask import redirect
from flask import send_from_directory
from flask import flash
from werkzeug import secure_filename
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
	databasename = song.write_to_database()
	#Return the exported page and attach the filename of the exported WAV file
	return render_template('exported.html', wavFileName=wavFileName, databasename=databasename)

@website.route('/return-file/<wavfilename>')
def return_file(wavfilename):
	directory = '{}/wav_outfiles/'.format(os.getcwd())
	return send_from_directory(directory, wavfilename, attachment_filename=wavfilename, as_attachment=True, mimetype='audio/wav')
	
@website.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():
   if request.method == 'POST':
      noteDict = {"C4":0, "D4":1, "E4":2, "F4":3, "G4":4, "A4":5, "B4":6, "C5":7}
      f = request.files['file']
      f.save(secure_filename(f.filename))
      song_read = Song()
      song_read.read_from_database(f.filename)
      notes_no = len(song_read.notes_to_play) / 2
      notes_to_set = [song_read.notes_to_play[i:i+2] for i in range(0, len(song_read.notes_to_play) - 1, 2)]
      values_to_set = [noteDict[i] for i in notes_to_set]
      print(values_to_set)
   return render_template('synth_uploaded.html', notes_no=notes_no, values_to_set=values_to_set)

@website.route('/return-db/<databasename>')
def return_db(databasename):
	directory = '{}/database_outfiles/'.format(os.getcwd())
	return send_from_directory(directory, databasename, attachment_filename=databasename, as_attachment=True)
