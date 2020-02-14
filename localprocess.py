import logging
import psycopg2
import psycopg2.extras
import bcrypt



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


def userLogin(username,password):

    try:
        conn = psycopg2.connect(host="localhost", port=5432, database="eticket", user="postgres", password="123")
        cur = conn.cursor(cursor_factory = psycopg2.extras.NamedTupleCursor)
    except Exception as e:
        logging.exception(e)
    try:
        cur.execute("""select 1 from eticket.users.userlogin where username=%s""", (username,))
        res = cur.fetchone()
        if res!=None:
            cur.execute("""select encode(password, 'escape') as password, user_id from eticket.users.userlogin where username = %s """, (username,))
            res=cur.fetchone()
            print(res)
            if bcrypt.checkpw(password.encode('utf8'),str.encode(res.password)):
                cur.close()
                return 'success'
            else:
                cur.close()
                return 'faild'
        else:
            cur.close()
            return 'faild'
        cur.close()
    except Exception as e:
        logging.exception(e)
