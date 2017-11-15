from flask import Flask
website = Flask(__name__)

from flask import g
from flask import render_template
from flask import request, url_for
from flask import redirect
from flask import send_from_directory
from flask import after_this_request
from werkzeug import secure_filename
from generator import Song
from preview_generator import Preview
import cloud_save
from flask import jsonify
import os
import datetime
import json
from validator import valid_cowbell_file
from platform import system


###########
#Global Variables Start
###########
SERVER_DB_NAME = 'cloud_save.db'
SERVER_DB_DIRECTORY = 'static/db'
###########
#Global Variables End
###########


#
#    VISIBLE PAGES
#

#HOMEPAGE/NOTE AMOUNT ENTER
@website.route('/')
def index():
    return render_template('index.html')

#NEW PROJECT PAGE
@website.route('/newproject', methods=['GET', 'POST'])
def newproject(error=None):
    if error:
        return render_template('newproject.html', error=error)
        
    if request.method == 'POST':
        noteamt = request.form.get('notes')
        if noteamt == "" or not int(noteamt):
            error = "Please enter a non-zero integer."
            return render_template('newproject.html', error=error)
        else:
            noteamt = abs(int(noteamt))
            return render_template('synth.html', notes=noteamt, notes_no=None, values_to_set=None, project_data=None)
    else:
        return render_template('newproject.html')

#EXISTING PROJECT PAGE
@website.route('/oldproject')
def oldproject():
    return render_template('oldproject.html')

#DISPLAYS WHEN WAV EXPORTED
def getNotes(rawSliderValues):
    #Dictionary of the slider values that correspond to the note values
    noteDict = {0:"C4", 1:"D4", 2:"E4", 3:"F4", 4:"G4", 5:"A4", 6:"B4", 7:"C5"}
    sliderValues = {}
    noteValues = []
    sliderKeys = []
    linked_notes_dict = {}
    linked_note_keys = []
    linked_notes = []
    
    #Extract the data from rawSliderValues and add it to sliderValues (Also get rid of "exporttowav")
    for key in rawSliderValues:
        if "slider" in key:
            temp_key = int(key[6:])
            sliderValues[temp_key] = rawSliderValues[key]
        elif "link" in key:
            temp_key = int(key[10:])
            linked_notes_dict[temp_key] = rawSliderValues[key]

    #Create a sorted list of the keys from slider values
    sliderKeys = sorted(sliderValues)
    linked_note_keys = sorted(linked_notes_dict)
    #  Get each note value from the noteDict in order using the sorted sliderKeys 
    #  list to call values from sliderValues in the original order
    for item in sliderKeys:
        noteValues.append(noteDict[int(sliderValues[item])])
    for item in linked_note_keys:
        linked_notes.append(noteDict[int(linked_notes_dict[item])])
    #Convert noteValues to string
    sNoteValues = ''.join(noteValues)
    str_linked_notes = ''.join(linked_notes)
    return([sNoteValues, str_linked_notes])

#DISPLAYS WHEN WAV EXPORTED
@website.route('/exported', methods=['GET', 'POST'])
def exported():
    #Get the submitted slider values from the previous page
    rawSliderValues = request.values if request.method == "GET" else request.values

    notes = getNotes(rawSliderValues)
    sNoteValues = notes[0]
    str_linked_notes = notes[1]

    jsondata = json.dumps({"songdata":sNoteValues, 
                        "linked_notes":str_linked_notes,
                        "author_name":'Anon', 
                        "outfile_name":None, 
                        "cloud_db_pos":None})
    #Return the exported page and attach the filename of the exported WAV file
    return render_template('exported.html', jsondata=jsondata)
#HELP PAGE
@website.route('/help')
def help_page():
    return render_template('help.html')

#LIST OF USERS PROJECTS (displays when user logs in)
@website.route('/projects', methods = ['GET', 'POST'])
def userprojects():
    if request.method == 'POST':
        uid = request.form.get('uid')
        g.cursor.execute("SELECT author_name FROM users WHERE UID = ?",(uid,))
        author_name = g.cursor.fetchall()
        if author_name == []:
            error = "UID not found"
            return render_template('oldproject.html', error=error)
        else:
            author_name = author_name[0][0]
            projects = cloud_save.list_projects(g.db, g.cursor, uid)
            return render_template("projects.html", author=author_name, projects=projects, uid=uid)
    else:
        return "Go back, you didn't enter a UID!"

@website.route('/manageaccount', methods = ['GET', 'POST'])
def manageaccount():
    if request.method == 'POST':
        UID = request.form.get('uid')
        user_data = cloud_save.get_user_data(g.db, g.cursor, UID)
        return render_template("manageaccount.html", UID=UID, user_data=user_data)




##
#    BACKEND ROUTES (downloading and uploading files, play and stop preview in synth)
##

# When a user is directed to this page, it downloads the file they request from the output directory
@website.route('/return-file/<wavfilename>')
def return_file(wavfilename):
    directory = '{}{}'.format(os.getcwd(),'/wav_outfiles/')
    @after_this_request
    def garbage_file(response):
        if system() == "Linux":
            os.remove('{}{}'.format(directory, wavfilename))
            return response
        else:
            return response
    return send_from_directory(directory, wavfilename, attachment_filename=wavfilename, as_attachment=True, mimetype='audio/wav')
    
@website.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():
    '''Handles the uploading of cowbell files'''
    if request.method == 'POST':
        noteDict = {"C4":0, "D4":1, "E4":2, "F4":3, "G4":4, "A4":5, "B4":6, "C5":7}
        f = request.files['file']
        f.save(secure_filename(f.filename))
        valid, error = valid_cowbell_file(f.filename)
        if not valid:
            os.remove(f.filename)
            return redirect('/oldproject')
        song_read = Song()
        song_read.read_from_database(f.filename)
        notes = len(song_read.notes_to_play) / 2
        notes_to_set = [song_read.notes_to_play[i:i+2] for i in range(0, len(song_read.notes_to_play) - 1, 2)]
        values_to_set = [noteDict[i] for i in notes_to_set]
    return render_template('synth.html', notes=notes, values_to_set=values_to_set, project_data=None)

@website.route('/return-db/<databasename>')
def return_db(databasename):
    '''When a user is directed to a page, the database that is specified is downloaded'''
    directory = '{}/database_outfiles/'.format(os.getcwd())
    @after_this_request
    def garbage_file(response):
        if system() == "Linux":
            os.remove('{}{}'.format(directory, databasename))
            return response
        else:
            return response
    return send_from_directory(directory, databasename, attachment_filename=databasename, as_attachment=True)


@website.route('/preview')
def preview_generator():
    '''Constructs a WAV file for preview on the synth page'''
    note_nums_temp = request.args.get('param_send', '00000000')
    note_nums = list(note_nums_temp)
    noteDict = {0:"C4", 1:"D4", 2:"E4", 3:"F4", 4:"G4", 5:"A4", 6:"B4", 7:"C5"}
    slider_values = []
    for note in note_nums:
            slider_values.append(noteDict[int(note)])
    slider_values_string = ''.join(slider_values)
    preview_song = Preview(slider_values_string)
    previewFileName = preview_song.make_wav()
    return jsonify(previewname=previewFileName)

@website.route('/downloader', methods=['GET', 'POST'])
def downloader():
    '''Manages the download of zips'''
    if request.method =="POST":
        returnedjson = request.form.get("returnedjson")
        returneddata = json.loads(returnedjson)
        
        # Generate the song from the json data
        #    REMEMBER TO ADD NOTE LINKING TO JSON

        song = Song(returneddata["songdata"], 'dummy', returneddata["author_name"], 'dummy',returneddata["outfile_name"], returneddata["cloud_db_pos"])
        

        if "audioformats" in request.form:
            #Create WAV file from the string version of noteValues
            # json_data = request.get_json()
            # print(type(json_data))
            #"songdata":sNoteValues, "author_name":'Anon', "outfile_name":None, "cloud_db_pos":None}
            #    REMEMBER TO ADD NOTE LINKING TO JSON
            
            wavFileName = song.make_wav(request.form.get("audioformats"))
            wavFileName = wavFileName.replace('wav_outfiles/','')

            return redirect('/return-file/{}'.format(wavFileName))


        elif "databasename" in request.form:

            databasename = song.write_to_database()
            return redirect('/return-db/{}'.format(databasename))

        elif "uid" in request.form:
            uid = request.form.get("uid")
            user_data = cloud_save.get_user_data(g.db, g.cursor, uid)
            if user_data is None:
                return render_template('exported.html', jsondata=returnedjson, message="User not found")
            else:
                user_ID = user_data[0]
            success = cloud_save.add_project(g.db, g.cursor, user_ID, song.notes_to_play, 
                                             song.creation_date, song.project_name)
            if success:
                return render_template('exported.html', jsondata=returnedjson, message="Song saved successfully")
            else:
                return render_template('exported.html', jsondata=returnedjson, message="Song could not be saved")
    return "You shouldn't be here. GO BACK!"

@website.route('/get_uid')
def get_uid():
    '''Generates a new UID and checks if its already in the database'''
    import uuid
    used_uids = cloud_save.get_uids(g.db, g.cursor)
    uid = uuid.uuid4().hex
    while uid in used_uids:
        uid = uuid.uuid4().hex
    cloud_save.add_user(g.db, g.cursor, uid)
    return jsonify(uid=uid)

@website.route('/get_project/<uid>', methods=['GET', 'POST'])
def get_project(uid):
    if request.method == "POST":
        project_ID = request.form.get("project_ID")
        project_data = cloud_save.open_project(g.db, g.cursor, uid, int(project_ID))
        noteDict = {"C4":0, "D4":1, "E4":2, "F4":3, "G4":4, "A4":5, "B4":6, "C5":7}
        song_read = Song(notes_to_play=project_data[0][1], author_name=project_data[0][2], project_name=project_data[0][4], cloud_db_pos=project_data[0][0])
        notes = len(song_read.notes_to_play) / 2
        notes_to_set = [song_read.notes_to_play[i:i+2] for i in range(0, len(song_read.notes_to_play) - 1, 2)]
        values_to_set = [noteDict[i] for i in notes_to_set]
        return render_template('synth.html', notes=notes, values_to_set=values_to_set, user_song=True, project_data=project_data)
    else:
        return "You shouldn't be here! Go back and select a project."

@website.route('/add_project/<uid>/<project_data>')
def add_project(uid, project_data):
    
    cloud_save.add_project()
    return None

@website.route('/get_projects/<uid>')
def get_project_list(uid):
    projects = cloud_save.list_projects(g.db, g.cursor, uid)
    return render_template('project_list.html', projects=projects, uid=uid)

@website.route('/changeuserdata', methods=['GET', 'POST'])
def changeuserdata():
    if request.method == 'POST':
        uid = request.form.get('uid')
        name = request.form.get('name')
        cloud_save.change_user_name(g.db, g.cursor, uid, name)
        return redirect('/projects', code=307)
    else:
        return "You should be here. Go back!"

###
#   Error Pages!
###
@website.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@website.errorhandler(Exception)
def all_exception_handler(e):
    time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    if not website.debug:
        website.logger.error("{}: {}".format(time,e))
        return render_template('error.html')
    else:
        return e

@website.errorhandler(500)
def unhandled_error(e):
    return render_template('500.html'), 500

@website.teardown_request
def close_database(exception):
    if hasattr(g, 'db') and hasattr(g, 'cursor'):
        cloud_save.close_database(g.db, g.cursor)

@website.before_request
def open_database():
    if not hasattr(g, 'db') or not not hasattr(g, 'cursor'):
        g.db, g.cursor = cloud_save.open_database(SERVER_DB_NAME, SERVER_DB_DIRECTORY)

if __name__ == "__main__":
	website.run()