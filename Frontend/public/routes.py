from flask import g
from flask import render_template
from flask import request
from flask import redirect
from public import website

@website.route('/', methods=['GET', 'POST'])
def index():
	error = None
	if request.method == 'POST':
		notes = request.form.get('notes')
		if notes == "":
			error = "Please enter a number."
		else:
			return redirect('/synth/{}'.format(notes))
	else:
		return render_template('index.html', error=error)

@website.route('/synth/<notes>')
def synth(notes = None):
	
	return render_template('synth.html', notes=notes)