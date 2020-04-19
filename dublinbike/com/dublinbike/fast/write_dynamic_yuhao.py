import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os
from pprint import pprint
import simplejson as json
import requests
import time
from IPython.display import display
import pandas as pd
import pymysql
import datetime

def get_dynamic():
    APIKEY = "9aad3ec0edbd53a6fb454f9f7e4ba503dadedd6b"
    NAME = "Dublin"
    STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
    r = requests.get(STATIONS_URI, params={"apiKey": APIKEY,"contract": NAME})
    text = json.loads(r.text)
    return text
    
def update_dynamic(lines):
    db = pymysql.connect("dbike.cerj203fcxcq.eu-west-1.rds.amazonaws.com", "yuhao", "qwert2008", "dbike")
    cursor = db.cursor()
    for text in lines:
        position = str(text['position']['lat']) + "," + str(text['position']['lng'])
        sql = "UPDATE dynamic_data SET status = %s, bike_stands = %s ,available_bike_stands = %s ,available_bikes = %s ,last_update = %s  WHERE position = %s"
        value=(text['status'],text['bike_stands'],text['available_bike_stands'],text['available_bikes'],text['last_update'],position)
        #sql="insert into dynamic_data(status,bike_stands,available_bike_stands,available_bikes,last_update,position) values (%s,%s,%s,%s,%s,%s)"
        cursor = db.cursor()
        cursor.execute(sql,value)
        db.commit()
        cursor.close()
while True:
    lines = get_dynamic()
    update_dynamic(lines)
    time.sleep(5*60)

