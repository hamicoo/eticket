import sqlite3
import logging
from flask import jsonify


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d




def checkemailvalidity(emailaddress):
    try:
        con = sqlite3.connect("database.db")
        con.row_factory = dict_factory
    except Exception as e:
        logging.exception(e)
    try:
        cur = con.cursor()
        query="select 1 from main.user_table where email='%s'"%(emailaddress)
        print(query)
        cur.execute(query)
        if cur.fetchone()!=None:
            return False
        else:
            return True
        cur.close()
    except Exception as e:
        logging.exception(e)



