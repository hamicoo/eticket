from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g

import sqlite3
import logging
import bcrypt
import localprocess
import re

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisisasecret!'


def connect_db():
	sql = sqlite3.connect('database.db')
	sql.row_factory = sqlite3.Row
	return sql


def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db


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


@app.route('/theform', methods=['GET'])
def theform():
	return render_template('form.html')


@app.route('/process', methods=['POST', 'GET'])
def process():
	myobh = {}
	name = request.form['name']
	family = request.form['family']
	email=request.form['email']
	nationalid = request.form['nationalid']
	birthdate = request.form['birthdate']
	sex = request.form['sex']
	mobile = request.form['mobile']
	password = request.form['password']

	myobh = {
			'result': 'Success!', 'resultCode': 1,
			 'name': name,
			 'family': family,
			'email':email,
			'nationalid':nationalid,
			 'birthdate': birthdate,
			 'sex':sex,
			 'mobile':mobile,
			 'password':password
			 }
	if checkemailvalidity(emailaddress=email):
		return render_template('confirmation.html', dataa=myobh)
	else:
		return jsonify({'error': 'Admin access is required'}), 401







@app.route("/checklogin", methods=['POST'])
def checklogin():
	username=request.form['email']
	password=request.form['password']
	result=localprocess.userLogin(username,password)

	return jsonify({'result':result})



@app.route('/check_email_jquery', methods=['GET', 'POST'])
def check_email_jquery():

		email=request.args.get('proglang')
		if not re.match(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", email):
			return jsonify(result='please enter correct email address')
		else:
			print(localprocess.checkemailvalidity(email))

			if localprocess.checkemailvalidity(email):
				return jsonify(result='you can register with this email address')
			else:
				return jsonify(result='it seem this email alredy in use please follow th link ')







@app.route('/interactive', methods=['GET', 'POST'])
def interactive():
	print('injaaaaaaaaaaaaaaaaaaaaaaaaa')
	try:
		return render_template('interactive.html')
	except Exception as e:
		return (str(e))












@app.route("/checkemailvalidity", methods=["GET,POST"])
def checkemailvalidity(emailaddress):
	return (localprocess.checkemailvalidity(emailaddress))






if __name__ == '__main__':
	app.run()
