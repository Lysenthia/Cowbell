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
	noteDict = {0:"C4", 1:"D4", 2:"E4", 3:"F4", 4:"G4", 5:"A4", 6:"B4", 7:"C5"}
	noteValues = []
	sliderValues = request.values if request.method == "GET" else request.values
	#response = "Form Contents <pre>%s</pre>" % "<br/>\n".join(["%s:%s" % item for item in formData.items()] )
	#sliderValues.pop('exporttowav', None)
	#THERE ARE MAJOR ERRORS HERE FIX IT
	for value in sliderValues:
		noteValues.append(noteDict[value])
	print(sliderValues)
	return "hi"
	#return render_template('exported.html')