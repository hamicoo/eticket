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



def getValidPlanList(is_student):
    if is_student==0:
        related_group=1
    else:
        related_group=2
    try:
        conn = psycopg2.connect(host="localhost", port=5432, database="eticket", user="postgres", password="123")
        cur = conn.cursor(cursor_factory = psycopg2.extras.NamedTupleCursor)
    except Exception as e:
        logging.exception(e)

    cur.execute(""" select id ,concat(name , ' Price :  ' , price ) from eticket.cards.cards_plan where related_group_type=%s order by price  """, (str(related_group)))

    res = cur.fetchall()

    return (res)



def getCurrentPlan(tag_id):
    try:
        conn = psycopg2.connect(host="localhost", port=5432, database="eticket", user="postgres", password="123")
        cur = conn.cursor(cursor_factory = psycopg2.extras.NamedTupleCursor)
    except Exception as e:
        logging.exception(e)
    query=""" select status from eticket.cards.online_cards where card_id={0} """.format(tag_id)
    cur.execute(query)
    res = cur.fetchone()
    print(res)
    print(res)
    if  res is None  :
        return True
    elif res.status ==1:
        return False

def getPlanActiveDays(PlanID):
        try:
            conn = psycopg2.connect(host="localhost", port=5432, database="eticket", user="postgres", password="123")
            cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        except Exception as e:
            logging.exception(e)
        query = """ select active_days from eticket.cards.cards_plan where id ='{0}' """.format(PlanID)

        cur.execute(query)
        res = cur.fetchone()
        if res is None:
            return (False,0)
        return (True,res.active_days)


def RegisterNewOnlineCard(user_id, card_id, plan_id, valid_to, status):

    try:
        conn = psycopg2.connect(host="localhost", port=5432, database="eticket", user="postgres", password="123")
        cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    except Exception as e:
        logging.exception(e)

    try:
        print('injaaaa')
        query = """ insert into eticket.cards.online_cards ( user_id, card_id, plan_id,valid_to, status) values ('{0}','{1}','{2}','{3}',{4} ) """.format(user_id,card_id,plan_id,valid_to,status)
        print(query)
        cur.execute(query)
        conn.commit()
        cur.close()
        return (True,'New Card Updated Successfully')
    except:
        return (False,'Error On Updating New Card')



def getCardHistory(user_id):

    try:
        conn = psycopg2.connect(host="localhost", port=5432, database="eticket", user="postgres", password="123")
        cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    except Exception as e:
        logging.exception(e)

    try:
        query = """ select user_id,card_id as tagid,cp.name,cp.price,cast(register_date as date),cast(ch.valid_to as date) , case when status=1 then 'Active' else 'Expired' end as Status from eticket.cards.cards_history ch join eticket.cards.cards_plan cp on ch.plan_id=cp.id where user_id='{}' """.format(user_id)
        cur.execute(query)
        res = cur.fetchall()
        cur.close()
        print(res)
        return True
    except:
        return False


