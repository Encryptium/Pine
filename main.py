from flask import Flask, render_template, request, redirect, session, jsonify, send_from_directory
import requests
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid
import random
import datetime

# Create the application instance
app = Flask(__name__, template_folder='templates')
app.config["SECRET_KEY"] = uuid.uuid4().hex

HOST = "https://pine.jonathan2018.repl.co"


demo_mode = True

@app.before_request
def make_session_permanent():
	session.permanent = True

	# Activate Demo Version
	if demo_mode:
		session['logged_in'] = True
		session['picture'] = "/static/images/icons/pfp.jpg"
		session['username'] = "demouser"
		session['email'] = "example@example.com"


# Functions
def generate_project_id():
	random_id = ''
	for i in range(15):
		random_id += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890")

	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	c.execute("SELECT * FROM projects WHERE id=:id", {"id": random_id})
	if c.fetchone() is not None:
		conn.close()
		return generate_project_id()
	conn.close()
	return random_id



# Index Page
@app.route('/')
def index():
	if 'logged_in' in session:
		return redirect('/discover')

	return render_template('index.html')


@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')

@app.route('/dashboard')
def dashboard():
	if 'logged_in' not in session:
		return redirect('/login?destination=' + request.path)

	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	c.execute("SELECT id, name, date FROM projects WHERE creator=:username", {"username": session['username']})
	projects = list(reversed(c.fetchall()))
	conn.commit()
	conn.close()

	return render_template('dashboard.html', projects=projects)

@app.route('/discover', methods=['POST', 'GET'])
def discover():
	if 'logged_in' not in session:
		return redirect('/login')

	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	projects = c.execute("SELECT * FROM projects WHERE id IS NOT 'hello'").fetchall()
	conn.commit()
	conn.close()

	random.shuffle(projects)
		
	return render_template('discover.html', projects=projects)

@app.route('/projects/create', methods=['POST', 'GET'])
def create_project():
	if 'logged_in' not in session:
		return redirect('/login?destination=' + request.path)

	if request.method == 'POST':
		name = request.form.get('project-name')
		creator = session['username']
		email = request.form.get('project-email')
		image = request.form.get('project-image') or '/static/images/default-banner.png'
		location = request.form.get('project-location')
		project_date = request.form.get('project-date')
		description = request.form.get('project-description')
		project_id = generate_project_id()

		conn = sqlite3.connect('db.sqlite3')
		c = conn.cursor()
		c.execute("INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (project_id, name, creator, email, image, location, project_date, description, session['username']))
		conn.commit()
		conn.close()
		return redirect('/project/'+project_id)

	current_date = datetime.date.today() - datetime.timedelta(1)

	return render_template('create_project.html', current_date=current_date)

@app.route('/edit/<project_id>', methods=['POST', 'GET'])
def edit_project(project_id):
	if 'logged_in' not in session:
		return redirect('/login?destination=' + request.path)
	
	if request.method == 'POST':
		name = request.form.get('project-name')
		email = request.form.get('project-email')
		location = request.form.get('project-location')
		project_date = request.form.get('project-date')
		description = request.form.get('project-description')
		
		conn = sqlite3.connect('db.sqlite3')
		c = conn.cursor()
		c.execute("SELECT creator FROM projects WHERE id=:project_id", {"project_id": project_id})

		if c.fetchone()[0] != session['username']:
			return "You can't edit a project that you don't own."
		else:
			pass

		c.execute("UPDATE projects SET name=:name, email=:email, location=:location, date=:project_date, description=:description WHERE id=:project_id", {"name": name, "email": email, "location": location, "project_date": project_date, "description": description, "project_id": project_id})
		conn.commit()
		conn.close()

	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	project_data = c.execute("SELECT * FROM projects WHERE id=:id", {"id": project_id}).fetchone()

	if not project_data:
		conn.commit()
		conn.close()
		return redirect('/dashboard')

	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	project_data = c.execute("SELECT * FROM projects WHERE id=:id", {"id": project_id}).fetchone()
	participant_count = len(project_data[8].split("|"))
	conn.commit()
	conn.close()	

	current_date = datetime.date.today() - datetime.timedelta(1)

	return render_template("edit.html", project=project_data, participant_count=participant_count, current_date=current_date)

@app.route('/participants/<project_id>')
def participants(project_id):
	if 'logged_in' not in session:
		return redirect('/login?destination=' + request.path)

	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
		
	creator = c.execute("SELECT creator FROM projects WHERE id=:project_id", {"project_id": project_id}).fetchone()[0]
	if session['username'] != creator:
		return "You can't view the participants of a project if you don't own it."
	
	project = c.execute("SELECT id, name FROM projects WHERE id=:project_id", {"project_id": project_id}).fetchone()
	participants = c.execute("SELECT participants FROM projects WHERE id=:project_id", {"project_id": project_id}).fetchone()[0].split("|")
	emails = []

	for participant in participants:
		emails.append(c.execute("SELECT email FROM users WHERE username=:username", {"username": participant}).fetchone()[0])
		
	conn.commit()
	conn.close()

	return render_template('participants.html', project=project, participants=participants, emails=emails)

@app.route('/project/<project_id>')
def project(project_id):
	if 'logged_in' not in session:
		return redirect('/login?destination=' + request.path)
	
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	project_data = c.execute("SELECT * FROM projects WHERE id=:id", {"id": project_id}).fetchone()

	if not project_data:
		conn.commit()
		conn.close()
		return redirect('/discover')

	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	project_data = c.execute("SELECT * FROM projects WHERE id=:id", {"id": project_id}).fetchone()
	participant_count = len(project_data[8].split("|"))
	participant_joined = "false"
	if session['username'] in project_data[8].split("|"):
		participant_joined = "true"

	conn.commit()
	conn.close()	
	return render_template('project.html', project=project_data, participant_count=participant_count, participant_joined=participant_joined)


@app.route('/api/v1/participate')
def participate():
	if 'logged_in' not in session:
		return redirect('/login')

	project_id = request.args.get('project_id')
	username = session['username']

	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	participants = c.execute("SELECT participants FROM projects WHERE id=:project_id", {"project_id": project_id}).fetchone()[0].split("|")
	participants.append(username)
	print(participants)
	participants = "|".join(participants)
	print(participants)
	c.execute("UPDATE projects SET participants=:participants WHERE id=:project_id", {"participants": participants, "project_id": project_id})
	conn.commit()
	conn.close()

	return jsonify({"status": "success", "message": "Joined"})


@app.route('/api/v1/remove/<project_id>')
def remove_participant(project_id):
	if 'logged_in' not in session:
		return redirect('/login')

	remove_user = request.args.get('remove')
	if remove_user == session['username']:
		return jsonify({"status": "failed", "message": "Cannot remove yourself"})
		
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	c.execute("SELECT creator FROM projects WHERE id=:project_id", {"project_id": project_id})
	if c.fetchone()[0] != session['username']:
		conn.commit()
		conn.close()
		return jsonify({"status": "failed", "message": "Invalid permissions"})
	else:
		pass

	participant_list = c.execute("SELECT participants FROM projects WHERE id=:project_id", {"project_id": project_id}).fetchone()[0].split("|")

	participant_list.remove(remove_user)
	participant_list = '|'.join(participant_list)

	c.execute("UPDATE projects SET participants=:participant_list WHERE id=:project_id", {"project_id": project_id, "participant_list": participant_list})
	conn.commit()
	conn.close()

	return jsonify({"status": "success", "message": "Participant Removed"})

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, debug=True)