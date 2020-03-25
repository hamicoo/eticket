import logging
import psycopg2
import psycopg2.extras
import bcrypt
import json





def checkcardvalidity(tagid,pinid):
    try:
        conn = psycopg2.connect(host="localhost", port=5432, database="eticket", user="postgres", password="123")
        cur = conn.cursor(cursor_factory = psycopg2.extras.NamedTupleCursor)
    except Exception as e:
        logging.exception(e)

    cur.execute("""select status from eticket.cards.all_cards where id=%s and pin=%s""", (tagid,pinid))
    res = cur.fetchone()

    if  res is None  :
        return False
    elif res.status ==1:
        return False
    return True





