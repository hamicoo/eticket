from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g,sessions
from markupsafe import escape
import sqlite3
import logging
import bcrypt
import gates,users,cards
import re
import os
import datetime


app = Flask(__name__)
app.secret_key = os.urandom(24)
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
myobh = {}

#SET timezone TO 'Asia/Tehran';






#PAGES
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    print('injaaa')
    return render_template('register.html')

@app.route('/confirm')
def confirm():
        if 'registeruser' in session:
            return render_template('confirmation.html', dataa=session['registeruser'])
        else:
            return render_template('register.html')




@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('examples/dashboard.html')
    return render_template('login.html')

@app.route('/user')
def user():
    if 'user_id' in session:
        return render_template('examples/user.html')
    return render_template('login.html')


@app.route('/cardPlan')
def cardPlan():
    avalibale_planes=cards.getValidPlanList(is_student=session['is_student'])
    getHistory=cards.getCardHistory(session['user_id'])
    cards.checkCardCredit(session['tagid'])
    if getHistory[0]:
        all_hist=getHistory[1]

    if cards.getCurrentPlan(session['tagid']):
        msg="you don't have any active plan on your card please select a plan to activate your card"
    else:
        msg="you already have an active plan on your card"
    return render_template('examples/cardPlan.html',server_list=avalibale_planes,message=msg,hist=all_hist)

#USER PROCESS SECTION

@app.route('/processNewRegisterUser', methods=['POST', 'GET'])
def process():
    myobh=[]

    name =   request.args.get('name')
    family = request.args.get('family')
    email=   request.args.get('proglang')
    nationalid = request.args.get('nationalid')
    birthdate = request.args.get('birthdate')
    sex = request.args.get('sex')
    mobile = request.args.get('mobile')
    password = request.args.get('password')
    address = request.args.get('address')
    city = request.args.get('city')
    pinid=request.args.get('pinid')
    tagid=request.args.get('tagid')
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
        return jsonify( {'code':'0','message': 'Your Card Information Is incorrect , please correct it before submit data', 'noticetype':'linear-gradient(to right, #eb5149, #fc190f)'})

    elif users.checkemailvalidity(emailaddress=email) is False:
        return jsonify({'code':'0','message': 'Your Email Addresss is incorrect' , 'noticetype':'linear-gradient(to right, #eb5149, #fc190f)'})
    else:
        session['registeruser'] = myobh
        return jsonify({'code':'1', 'message': 'everything seem to be good just conform it !','noticetype': 'linear-gradient(to right, #00b09b, #96c93d)'})
        #return render_template('confirmation.html', dataa=myobh)







@app.route("/checkemailvalidity", methods=["GET,POST"])
def checkemailvalidity(emailaddress):
    return (users.checkemailvalidity(emailaddress))


@app.route('/check_email_jquery', methods=['GET', 'POST'])
def check_email_jquery():
        app.logger.debug('A value for debugging')

        email=request.args.get('proglang')

        if not re.match(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", email):
            return jsonify(result='2')
        else:
            if users.checkemailvalidity(email):
                return jsonify(result='1')
            else:
                return jsonify(result='0')


@app.route("/checklogin", methods=['POST'])
def checklogin():

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
        session['is_student']=result[1].is_student
        cards.getValidPlanList(session['is_student'])
        return redirect(url_for('dashboard'))

    return jsonify({'result':'login Failed'})


@app.route("/registeruser", methods=['POST'])
def registeruser():

    if users.registerNewUser(userinfo=session['registeruser']):
        return render_template('login.html')
    else:
        return render_template('404.html', title='404'), 404


@app.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

    #return render_template('login.html')


#CARDS



@app.route('/check_tagid', methods=['GET', 'POST'])
def check_tagid():
    pinid=request.args.get('pinid')
    tagid=request.args.get('tagid')
    res=cards.checkcardvalidity(tagid,pinid)
    return jsonify(result=str(res))


@app.route('/updatecardplan', methods=['GET', 'POST'])
def updatecardplan():
    PlaneId=request.form['option']
    active_days=cards.getPlanActiveDays(PlaneId)
    if active_days[0]:
            EndDate = datetime.date.today() + datetime.timedelta(days=active_days[1])
            res=cards.RegisterNewOnlineCard(user_id=session['user_id'],card_id=session['tagid'],plan_id=PlaneId,valid_to=EndDate,status=1)
            return redirect(url_for('cardPlan'))
    else:
            return jsonify(result='your Selected Plan is Invalid ! ')







#GATES

@app.route('/testcode')
def testcode():
    return render_template('testcode.html')

@app.route('/get_word')
def get_prediction():
  word = request.args.get('word')
  return jsonify({'html': str((word))})


#TEST

@app.route('/mainpage', methods=['GET'])
def mainpage():

    if 'userid' in session:
        return 'Logged in as %s' % escape(session['userid'])
    return 'You are not logged in'


if __name__ == '__main__':
    app.run(debug=True,port=1265)


