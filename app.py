from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
import sqlite3
import bcrypt

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisisasecret!'


def connect_db():
	sql = sqlite3.connect('database.db')

	def dict_factory(cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d
	sql.row_factory = dict_factory
	return sql


def get_db():
	if not hasattr(g, 'sqlite3'):
		g.sqlite_db = connect_db()
	return g.sqlite_db


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
	nationalid = request.form['nationalid']
	birthdate = request.form['birthdate']
	sex = request.form['sex']
	mobile = request.form['mobile']
	password = request.form['password']

	myobh = {
			'result': 'Success!', 'resultCode': 1,
			 'name': name,
			 'family': family,
			'nationalid':nationalid,
			 'birthdate': birthdate,
			 'sex':sex,
			 'mobile':mobile,
			 'password':password
			 }

	return render_template('confirmation.html', dataa=myobh)


@app.route('/checklogin', methods=['POST'])
def checklogin():
	print(request.form)
	connect_db()
	db = get_db()
	query=("select id, user_id, username, password, locksts, lastlogin, temppass, forgetsts " 
	 		"from user_login "
	 		 "where username='{0}' ".format(request.form['email']))

	cur = db.execute(query)
	results = cur.fetchone()
	print(results['username'])

	return jsonify({'email':request.form['email'],'password':request.form['password']})
	#if request.method == 'POST':
	#	print('post')
	#	new = request.form.get('email', 'default')
	# body=request.form['password']
	#	print(new)


# mail = request.form['email']
# password = request.form['password']
# print(mail,password)
#

#


# return '<h1>The ID is {}. The name is {}. The location is {}.</h1>'.format(results[0]['id'], results[0]['name'],
#																		   results[0]['location'])


# print(mail,password)
#   return jsonify({'name':1})


# return render_template('confirmation.html', dataa=myobh)


if __name__ == '__main__':
	app.run()
