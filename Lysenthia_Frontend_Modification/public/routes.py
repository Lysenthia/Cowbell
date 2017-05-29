from flask import g
from flask import render_template
from flask import request
from flask import redirect
from flask import send_from_directory
from public import website
from generator import make_wav
import os

#HOMEPAGE/NOTE AMOUNT ENTER
@website.route('/', methods=['GET', 'POST'])
def index():
        error = None
        if request.method == 'POST':
                noteamt = request.form.get('notes')
		# THIS MAKES AN ERROR FIX IT UP AT SOME POINT PLZZ
                if noteamt == "":
                        error = "Please enter a number."
                else:
                        return redirect('/synth/{}'.format(noteamt))
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
        noteDict = dict(((0, "C4"), (1, "D4"), (2, "E4"), (3, "F4"), (4, "G4"), (5, "A4"), (6, "B4"), (7, "C5")))
        slider_values_true = {}
        note_values = []
        sliderValues = request.values if request.method == "GET" else request.values
        for key in sliderValues:
                if key != "exporttowav":
                        print(key)
                        slider_values_true[key] = sliderValues[key]
        sliderKeys = sorted(slider_values_true)
        for item in sliderKeys:
                note_values.append(noteDict[int(slider_values_true[item])])
        string = ''.join(note_values)
        outfile_name = make_wav(string)
#        if request.method == 'POST':
#                return redirect('/return-file/{}'.format(outfile_name))
#        else:
#               return render_template('exported.html', outfile_name = outfile_name)
        return render_template('exported.html', outfile_name = outfile_name)
    

@website.route('/return-file/<outfile_name>')
def return_file(outfile_name):
    outfile_name = outfile_name
    directory = os.getcwd()
    return send_from_directory(directory, outfile_name, 
                     attachment_filename=outfile_name,
                     as_attachment=True, mimetype='audio/wav')
