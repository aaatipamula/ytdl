import sqlite3
from datetime import datetime as dt
import json
import os
from tkinter import W

settings = json.load(open('./discord_bot/settings.json'))

def tester(time :str):
    time_string = time
    tim = dt.utcnow()
    tim_now = tim.strftime('%H.%d.%m')
    
    time_list = time.split('.')
    time_list = [int(x) for x in time_list] 

    vals = tim_now.split('.')
    vals = [int(x) for x in vals]    
    
    def deleter():
        connection = sqlite3.connect(settings.get('db_source'))
        cursor = connection.cursor()

        a = cursor.execute(f"SELECT * FROM ids WHERE tim = \'{time_string}\'")
        cursor.execute(f"DELETE FROM ids WHERE tim = \'{time_string}\'")

        connection.commit()
        connection.close()    
       
        b = [x[1] for x in b]
        string_arr = b[1].split('$') 
        
        os.remove(settings.get(f'{string_arr[1]}_dir') + string_arr[0] + '.' + string_arr[1])

    def checker(tim_now :list, time_list :list):
    
        if tim_now[2] > time_list[2]:
            deleter()
        elif tim_now[2] == time_list[2]:

            if tim_now[1] > time_list[1]:
                deleter()
            elif tim_now[1] == time_list[1]:

                if tim_now[0] >= time_list[0]:
                    deleter()
    
    checker(vals, time_list)

def main():        
    connection = sqlite3.connect(settings.get('db_source'))
    cursor = connection.cursor()

    vals = [x[2] for x in cursor.execute('SELECT * FROM ids')]

    connection.commit()
    connection.close()

    for x in vals:
        tester(x)

if __name__ == '__main__':
    main()