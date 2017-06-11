from flask import g
from flask import render_template
from flask import request
from flask import redirect
from public import website

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
        print(noteDict)

        #Values of the sliders once they come out
        slider_values_true = {}
        #List of inputted notes after they've been converted from the slider values
        note_values = []
        #get the slider values from the page
        sliderValues = request.values if request.method == "GET" else request.values
        #Extract data from the slider values and remove "exporttowav"
        for key in sliderValues:
                if key != "exporttowav":
                        print(key)
                        slider_values_true[key] = sliderValues[key]
        print(slider_values_true)
        #Adding the corresponding slider values to the note values
        for item in list(slider_values_true.values()):
                note_values.append(noteDict[int(item)])
        print(note_values)
        #Pretty it up
        string = ''.join(note_values)
        #This will eventually not return as a string
        return string
