import sqlite3
import json
import base64
import random
from datetime import datetime as dt

settings = json.load(open('./discord_bot/settings.json'))

def query_select(query :str, column :int):

    connection = sqlite3.connect(settings.get("db_source"))
    cursor = connection.cursor()

    a = cursor.execute(query)    
    b = [x[column] for x in a]

    connection.commit()
    connection.close()

    return b

def query_insert(query :str, vals :tuple):

    connection = sqlite3.connect(settings.get("db_source"))
    cursor = connection.cursor()

    cursor.execute(query, vals)    
    
    connection.commit()
    connection.close()

def check_contentids(id :str):

    a = query_select(f'SELECT * FROM ids WHERE idone = \'{id}\'', 1)
    
    if id in a:
        
        b = query_select(f'SELECT * FROM ids WHERE idone = \'{id}\'', 0) 
        
        return b[0]

    else: return None
        

def dump_id(content_id :str):

    req_id = base64.urlsafe_b64encode(str(random.choice(range(1, 999999))).encode('utf-8')).decode('utf-8')
    
    a = query_select(f"SELECT * FROM ids WHERE reqids = \'{req_id}\'", 0)
    
    if req_id in a:
        
        req_id = base64.urlsafe_b64encode(str(random.choice(range(1, 999999))).encode('utf-8')).decode('utf-8')
    
    t = dt.utcnow()

    try:
        curr_time = t.replace(day=t.day + 1).strftime('%H.%d.%m')
    except ValueError:
        curr_time = t.replace(day=1, month=t.month + 1).strftime('%H.%d.%m')
    
    query_insert("INSERT INTO ids (reqids, idone, tim) VALUES (?, ?, ?)", (req_id, content_id, curr_time))
    
    return req_id