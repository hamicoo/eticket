from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g,sessions
from markupsafe import escape
import sqlite3
import logging
import bcrypt
import gates,users,cards
import re
import os
import kavenegar




app = Flask(__name__)
app.secret_key = os.urandom(24)

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


myobh = {}


#PAGES

@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html', title='404'), 404

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/userprofile')
def userprofile():
	return render_template('userprofile.html')

@app.route('/theform', methods=['GET'])
def theform():
	return render_template('form.html')



@app.route('/dashboard')
def dashboard():

	return render_template('examples/dashboard.html')

@app.route('/user')
def user():
	global myobh

	if len(myobh)<2:

		return render_template('login.html')
	return render_template('examples/user.html')

#USER PROCESS SECTION

@app.route('/processNewRegisterUser', methods=['POST', 'GET'])
def process():
	global myobh

	name = request.form['name']
	family = request.form['family']
	email=request.form['proglang']
	nationalid = request.form['nationalid']
	birthdate = request.form['birthdate']
	sex = request.form['sex']
	mobile = request.form['mobile']
	password = request.form['password']
	address = request.form['address']
	city = request.form['city']
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
			 'address' : address,
			'city': city,
			'tagid': tagid,
			'pinid' : pinid
			 }
	if cards.checkcardvalidity(tagid,pinid) is  False:
		return jsonify({'error': 'Your Pin or Tag Id Is Incorrect'}), 401

	if users.checkemailvalidity(emailaddress=email) is False:
		return jsonify({'error': 'Your Email Addresss is incorrect'}), 401

	return render_template('confirmation.html',dataa=myobh)


@app.route("/checkemailvalidity", methods=["GET,POST"])
def checkemailvalidity(emailaddress):
	return (users.checkemailvalidity(emailaddress))


@app.route('/check_email_jquery', methods=['GET', 'POST'])
def check_email_jquery():
		app.logger.debug('A value for debugging')

		email=request.args.get('proglang')

		if not re.match(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", email):
			return jsonify(result='please enter correct email address')
		else:
			if users.checkemailvalidity(email):
				return jsonify(result='you can register with this email address')
			else:
				return jsonify(result='it seem this email alredy in use please follow th link ')


@app.route("/checklogin", methods=['POST'])
def checklogin():
	global myobh
	username=request.form['email']
	password=request.form['password']
	result=users.userLogin(username,password)
	if result[0]=='success':
		logging.warning(result[1].name + ' logged in ')
		myobh=result[1]
		session['user_id'] = result[1].user_id
		session['name'] = result[1].name
		session['family'] = result[1].family
		session['birthdate'] = str(result[1].birthdate)
		session['registerdate'] = str(result[1].registerdate)
		session['sex'] = result[1].sex
		session['email'] = result[1].email
		session['mobile'] = result[1].mobile
		session['address'] = result[1].address
		session['lastlogin'] = str(result[1].lastlogin)
		session['tagid'] = result[1].tagid
		session['pinid'] = result[1].pinid


		return render_template('examples/dashboard.html')

	return jsonify({'result':'login Failed'})


@app.route("/registeruser", methods=['POST'])
def registeruser():
	global myobh
	if users.registerNewUser(userinfo=myobh):
		return render_template('login.html')
	else:
		return render_template('404.html', title='404'), 404




#CARDS



@app.route('/check_tagid', methods=['GET', 'POST'])
def check_tagid():
	pinid=request.args.get('pinid')
	tagid=request.args.get('tagid')
	res=cards.checkcardvalidity(tagid,pinid)
	return jsonify(result=str(res))


#GATES


#TEST

@app.route('/mainpage', methods=['GET'])
def mainpage():

	if 'userid' in session:
		return 'Logged in as %s' % escape(session['userid'])
	return 'You are not logged in'


if __name__ == '__main__':

	app.run(debug=True)

