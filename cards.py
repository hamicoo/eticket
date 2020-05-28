import logging
import psycopg2
import psycopg2.extras
import redis
from datetime import date
import json










try:
    rediss = redis.Redis('localhost')
    rediss.flushdb()
except Exception as e:
    print(str(e))



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


        query = """ insert into eticket.cards.online_cards ( user_id, card_id, plan_id,valid_to, status) values ('{0}','{1}','{2}','{3}',{4} ) """.format(user_id,card_id,plan_id,valid_to,status)
        cur.execute(query)
        conn.commit()



        query=""" select card_id,concat(name,' ',family) as names,
        date_part('day',age(valid_to,now() )) as remaining_days,
        case when date_part('day',age(valid_to,now() )) <0  then 0 else 1 end as status  from eticket.cards.online_cards
        join users.userinfo on online_cards.user_id = userinfo.id and  online_cards.card_id={} """.format(card_id)
        cur.execute(query)
        res=cur.fetchone()
        myobj = {}
        myobj['card_id'] = res.card_id
        myobj['owner'] = res.names
        myobj['remain'] = res.remaining_days
        myobj['status'] = res.status
        rediss.set(res.card_id, json.dumps(myobj))


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
        query=""" update eticket.cards.online_cards set status=0 where user_id='{}' and cast(valid_to as date)<cast(now() as date)  """.format(user_id)
        cur.execute(query)
        conn.commit()
        query= """ insert into eticket.cards.cards_history select * from eticket.cards.online_cards where user_id='{}' and status=0 """.format(user_id)
        cur.execute(query)
        conn.commit()
        query=""" delete from eticket.cards.online_cards where user_id='{}' and status=0 """.format(user_id)
        cur.execute(query)
        conn.commit()
    except Exception as e:
        logging.warning(e)
        cur.close()
        return (False,'Error 122')


    try:
        query = """ select * from 
                    (select card_id as tagid,cp.name,cp.price,cast(register_date as date),cast(ch.valid_to as date) , case when status=1 then 'Active' else 'Expired ' end as Status 
                    from eticket.cards.online_cards ch join eticket.cards.cards_plan cp on ch.plan_id=cp.id where user_id='{0}' 
                        union all
                    select card_id as tagid,cp.name,cp.price,cast(register_date as date),cast(ch.valid_to as date) , case when status=1 then 'Active' else 'Expired ' end as Status 
                    from eticket.cards.cards_history ch join eticket.cards.cards_plan cp on ch.plan_id=cp.id where user_id='{0}')res
                    order by res.Status ASC """.format(user_id)
        cur.execute(query)
        res = cur.fetchall()
        cur.close()
        return (True,res)
    except:
        return (False,'Error 141 - When Fetch Card History')



def checkCardCredit(tag_id):
    curDate=date.today()
    try:
        conn = psycopg2.connect(host="localhost", port=5432, database="eticket", user="postgres", password="123")
        cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    except Exception as e:
        logging.exception(e)
        return (False, str(e))

    try:
        query = """ select top 1  cast(valid_to as date),status from  eticket.cards.online_cards where card_id='{}' """.format(tag_id)
        cur.execute(query)
        res = cur.fetchone()

        if  res.valid_to >= curDate :
            cur.close()
            return (True,'Open The Gate')

        if res==None :
            cur.close()
            return (False,'You Have No Active Plan')

        if  res.valid_to < curDate and res.status==0:
            cur.close()
            return (False,'Expired Credit')

        if  res.valid_to < curDate and res.status==1:
            try:
                query = """ update eticket.cards.online_cards set status=0 where card_id='{}' """.format(tag_id)
                cur.execute(query)
                conn.commit()
                cur.close()
            except Exception as e:
                logging.warning(e)
                return (False, str(e))

            cur.close()
            return (False,'Expired Credit')
    except Exception as e:
        logging.warning(e)
        return (False,str(e))
