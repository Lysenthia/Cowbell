from flask import g
from flask import render_template
from flask import request
from flask import redirect
from public import website

@website.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		notes = request.form.get('notes')
		return redirect('/synth/{}'.format(notes))
	else:
		return render_template('index.html')

@website.route('/synth/<notes>')
def synth(notes = None):
	
	return render_template('synth.html', notes=notes)