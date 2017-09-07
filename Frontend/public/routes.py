from flask import g
from flask import render_template
from flask import request
from flask import redirect
from flask import send_from_directory
from flask import flash
from werkzeug import secure_filename
from public import website
from generator import Song
from preview_generator import Preview
import cloud_save
from flask import jsonify, request
import os
import json
import sqlite3

###########
#Global Variables Start
###########
SERVER_DB_NAME = 'cloud_save.db'
SERVER_DB_DIRECTORY = 'public/static/db'
###########
#Global Variables End
###########


#
#    VISIBLE PAGES
#

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
	if request.method == 'GET':
		print("Sup")
	return render_template('synth.html', notes=notes)


#DISPLAYS WHEN WAV EXPORTED
@website.route('/exported', methods=['GET', 'POST'])
def exported():
	# if "audioformats" in request.form:
	# 	audioformat = request.form.get("audioformats")
	# 	return redirect('downloader/audiofile/{}'.format(audioformat))

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
			print(key)
			temp_key = int(key[6:])
			sliderValues[temp_key] = rawSliderValues[key]

	#Create a sorted list of the keys from slider values
	sliderKeys = sorted(sliderValues)
	print(sliderKeys)
	#  Get each note value from the noteDict in order using the sorted sliderKeys 
	#  list to call values from sliderValues in the original order
	for item in sliderKeys:
		noteValues.append(noteDict[int(sliderValues[item])])

	#Convert noteValues to string
	sNoteValues = ''.join(noteValues)
	jsondata = json.dumps({"songdata":sNoteValues, "author_name":'Anon', "outfile_name":None, "cloud_db_pos":None})
	print("JSON: ".format(jsondata))
	print(type(jsondata))
	#Return the exported page and attach the filename of the exported WAV file
	return render_template('exported.html', jsondata=jsondata)

#HELP PAGE
@website.route('/help')
def help():
	return render_template('help.html')

@website.route('/projects', methods = ['GET', 'POST'])
def userprojects():
	if request.method == 'POST':
		uid = request.form.get('uid')
		db = sqlite3.connect('{}/{}'.format(SERVER_DB_DIRECTORY, SERVER_DB_NAME))
		cursor = db.cursor()
		cursor.execute("SELECT author_name FROM users WHERE UID = ?",(uid,))
		author_name = cursor.fetchall()
		author_name = author_name[0][0]
		projects = cloud_save.list_projects(SERVER_DB_NAME, SERVER_DB_DIRECTORY, uid)
		print(type(uid))
		print(projects)
		print(type(author_name))
		return render_template("projects.html", author=author_name, projects=projects, uid=uid)
	else:
		return "Go back, you didn't enter a UID!"














# When a user is directed to this page, it downloads the file they request from the output directory
@website.route('/return-file/<wavfilename>')
def return_file(wavfilename):
	directory = '{}{}'.format(os.getcwd(),'/wav_outfiles/')
	return send_from_directory(directory, wavfilename, attachment_filename=wavfilename, as_attachment=True, mimetype='audio/wav')
	
# Handles the uploading of cowbell files
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

@website.route('/preview')
def preview_generator():
		print("IN PREVIEW")
		note_nums_temp = request.args.get('param_send', '00000000')
		note_nums = list(note_nums_temp)
		noteDict = {0:"C4", 1:"D4", 2:"E4", 3:"F4", 4:"G4", 5:"A4", 6:"B4", 7:"C5"}
		slider_values = []
		for note in note_nums:
				slider_values.append(noteDict[int(note)])
		slider_values_string = ''.join(slider_values)
		preview_song = Preview(slider_values_string)
		previewFileName = preview_song.make_wav()
		previewFileName = previewFileName.replace('public','..')
		return jsonify(previewname=previewFileName)

@website.route('/downloader', methods=['GET', 'POST'])
def downloader():
	if request.method =="POST":
		if "audioformats" in request.form:
			if request.form.get("audioformats") == "wav":
				#Create WAV file from the string version of noteValues
				# json_data = request.get_json()
				# print(type(json_data))
				returnedjson = json.loads(request.form.get("returnedjson"))
				#"songdata":sNoteValues, "author_name":'Anon', "outfile_name":None, "cloud_db_pos":None}
				song = Song(None)
				wavFileName = song.make_wav()
				wavFileName = wavFileName.replace('wav_outfiles/','')
				databasename = song.write_to_database()
				#return redirect('/return-file/{}'.format(filename))


		elif action == "cowbellfile":
			return redirect('/return-db/{}'.format(filename))
	return "You shouldn't be here. GO BACK!"

@website.route('/get_uid')
def get_uid():
	import uuid
	used_uids = cloud_save.get_uids(SERVER_DB_NAME, SERVER_DB_DIRECTORY)
	uid = uuid.uuid4().hex
	while uid in used_uids:
		uid = uuid.uuid4().hex
	cloud_save.add_user(SERVER_DB_NAME, SERVER_DB_DIRECTORY, uid)
	print(uid)
	return jsonify(uid=uid)
	
@website.route('/get_project/<uid>/<project_to_open>')
def get_project(uid, project_to_open):
	project_data = cloud_save.open_project(SERVER_DB_NAME, SERVER_DB_DIRECTORY, uid, project_to_open)
	noteDict = {"C4":0, "D4":1, "E4":2, "F4":3, "G4":4, "A4":5, "B4":6, "C5":7}
	song_read = Song(project_data[1], project_data[2], project_data[4], project_data[0])
	notes_no = len(song_read.notes_to_play) / 2
	notes_to_set = [song_read.notes_to_play[i:i+2] for i in range(0, len(song_read.notes_to_play) - 1, 2)]
	values_to_set = [noteDict[i] for i in notes_to_set]
	print(values_to_set)
	return render_template('synth_uploaded.html', notes_no=notes_no, values_to_set=values_to_set)

@website.route('/add_project/<uid>/<project_data>')
def add_project(uid, project_data):
	
	cloud_save.add_project()
	return None

@website.route('/get_projects/<uid>')
def get_project_list(uid):
	projects = cloud_save.list_projects(SERVER_DB_NAME, SERVER_DB_DIRECTORY, uid)
	return render_template('project_list.html', projects=projects, uid=uid)