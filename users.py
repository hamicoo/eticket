import logging
import psycopg2
import psycopg2.extras
import bcrypt
import json




def checkemailvalidity(emailaddress):
    try:
        conn = psycopg2.connect(host="localhost", port=5432, database="eticket", user="postgres", password="123")
        cur = conn.cursor(cursor_factory = psycopg2.extras.NamedTupleCursor)
    except Exception as e:
        logging.exception(e)
    try:
        cur.execute("""select 1 from eticket.users.userinfo where email=%s""", (emailaddress,))
        res = cur.fetchone()
        if res!=None:
            return False
        else:
            return True
        cur.close()
    except Exception as e:
        logging.exception(e)


def userLogin(username, password):
    try:
        conn = psycopg2.connect(host="localhost", port=5432, database="eticket", user="postgres", password="123")
        cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

    except Exception as e:
        logging.exception(e)
    try:
        cur.execute("""select 1 from eticket.users.userlogin where username=%s""", (username,))
        res = cur.fetchone()
        if res != None:

            cur.execute("""select encode(password, 'escape') as password, user_id,name,family,birthdate,sex,mobile,email,
                            address,registerdate,lo.lastlogin,ca.id as tagid,ca.pin as pinid
                                from eticket.users.userlogin lo
                                    join eticket.users.userinfo inf on lo.user_id=inf.id
                                join eticket.cards.all_cards ca on lo.user_id=ca.owner_user_id
                            where username = %s """, (username,))
            userinfo = cur.fetchone()
            logging.info(userinfo)
            if bcrypt.checkpw(password.encode('utf8'), str.encode(userinfo.password)):
                cur.close()
                updateLoginTime(userinfo.user_id)

                return ('success', userinfo)
            else:
                cur.close()
                return ('faild', None)
        else:
            cur.close()
            return ('faild', None)
        cur.close()
    except Exception as e:
        logging.exception(e)




def updateLoginTime(userId):
    try:
        conn = psycopg2.connect(host="localhost", port=5432, database="eticket", user="postgres", password="123")
        cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    except Exception as e:
        logging.exception(e)
    cur.execute("""update eticket.users.userlogin set lastlogin=now()::timestamp(0) where user_id= %s """, (userId,))
    conn.commit()
    cur.close()
    return True





def registerNewUser(userinfo):
    print('userinfo function')


    try:
        conn = psycopg2.connect(host="localhost", port=5432, database="eticket", user="postgres", password="123")
        cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    except Exception as e:
        logging.exception(e)




    try:
        cur.execute(
            """ INSERT INTO "users"."userinfo" ("id", "name", "family", "birthdate", "sex", "mobile", "email", "address", "registerdate") 
                VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, DEFAULT) returning id """,
            (userinfo['name'], userinfo['family'], userinfo['birthdate'],userinfo['sex'],userinfo['mobile'],userinfo['email'],userinfo['address']))
        inserted_user_id=cur.fetchone()
        try:
            salt = bcrypt.gensalt()
            encryptedPassword = bcrypt.hashpw(userinfo['password'].encode('utf8'), salt)
            cur.execute(
                """ INSERT INTO "users"."userlogin" ("id", "user_id", "username", "password")
                 VALUES (DEFAULT, %s, %s, %s ) """,
                (inserted_user_id, userinfo['email'], encryptedPassword))
            try:
                salt = bcrypt.gensalt()
                encryptedPassword = bcrypt.hashpw(userinfo['password'].encode('utf8'), salt)
                cur.execute(
                    """ update cards.all_cards set owner_user_id=%s , status=1 , update_date=now() where id=%s and pin=%s  """,
                    (inserted_user_id,userinfo['tagid'] ,userinfo['pinid'] ))
            except Exception as e:
                logging.exception(e)
        except Exception as e:
            logging.exception(e)
    except Exception as e:
        logging.exception(e)


    try:
        conn.commit()
        cur.close()
        return 'inserted success !'

    except Exception as e:
        logging.exception(e)








