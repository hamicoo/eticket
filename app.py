from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g,sessions
from markupsafe import escape
import sqlite3
import logging
import bcrypt
import gates,users,cards
import re




app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisisasecret!'
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')






def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d


@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()


@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html', title='404'), 404


@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/userprofile')
def userprofile():
	return render_template('userprofile.html')


@app.route('/theform', methods=['GET'])
def theform():

	return render_template('form.html')


@app.route('/mainpage', methods=['GET'])
def mainpage():
	print(session)
	if 'userid' in session:
		return 'Logged in as %s' % escape(session['userid'])
	return 'You are not logged in'


@app.route('/process', methods=['POST', 'GET'])
def process():
	myobh = {}
	name = request.form['name']
	family = request.form['family']
	email=request.form['proglang']
	nationalid = request.form['nationalid']
	birthdate = request.form['birthdate']
	sex = request.form['sex']
	mobile = request.form['mobile']
	password = request.form['password']
	pinid=request.form['pinid']
	tagid=request.form['tagid']

	myobh = {
			'result': 'Success!',
			'resultCode': 1,
			 'name': name,
			 'family': family,
			'email':email,
			'nationalid':nationalid,
			 'birthdate': birthdate,
			 'sex':sex,
			 'mobile':mobile,
			 'password':password,
			'tagid': tagid,
			'pinid' : pinid
			 }

	if cards.checkcardvalidity(tagid,pinid) is  False:
		return jsonify({'error': 'Your Pin or Tag Id Is Incorrect'}), 401

	if users.checkemailvalidity(emailaddress=email) is False:
		return jsonify({'error': 'Your Email Addresss is incorrect'}), 401

	return render_template('confirmation.html', dataa=myobh)








@app.route("/checklogin", methods=['POST'])
def checklogin():
	username=request.form['email']
	password=request.form['password']
	result=users.userLogin(username,password)
	if result[0]=='success':
		logging.warning(result[1].name + ' logged in ')

		return render_template('userprofile.html', dataa=result[1])
	return jsonify({'result':'login Failed'})





@app.route('/check_email_jquery', methods=['GET', 'POST'])
def check_email_jquery():
		app.logger.debug('A value for debugging')

		email=request.args.get('proglang')

		if not re.match(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", email):
			return jsonify(result='please enter correct email address')
		else:
			print(users.checkemailvalidity(email))

			if users.checkemailvalidity(email):
				return jsonify(result='you can register with this email address')
			else:
				return jsonify(result='it seem this email alredy in use please follow th link ')
















@app.route("/checkemailvalidity", methods=["GET,POST"])
def checkemailvalidity(emailaddress):
	return (users.checkemailvalidity(emailaddress))




@app.route('/check_tagid', methods=['GET', 'POST'])
def check_tagid():
	pinid=request.args.get('pinid')
	tagid=request.args.get('tagid')
	res=cards.checkcardvalidity(tagid,pinid)

	return jsonify(result=str(res))





if __name__ == '__main__':
	app.run()
