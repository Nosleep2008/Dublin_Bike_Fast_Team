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
'''
def getWeather():  
    url = "https://samples.openweathermap.org/data/2.5/weather?lat=35&lon=139&appid=d70c2aeec07fd23450a7b6e887b9b336" 
    info = requests.get(url).json()
    return info
print(getWeather())
'''


def get_static():
    with open('./dublin.json', 'r') as f:
        text = json.load(f)  
    return text
 
def insert_static(lines):
    for text in lines:
        db = pymysql.connect("dbbike.cponz0wamutb.eu-west-1.rds.amazonaws.com", "junyi", "db123456", "dbbike")
        cursor = db.cursor()
        position = str(text['latitude']) + "," + str(text['longitude'])
        value=(text['number'],text['name'],text['address'],position)
        sql="insert into static_data(number,station_name,address,position) values (%s,%s,%s,%s)"
        cursor = db.cursor()
        cursor.execute(sql,value)
        db.commit()
        cursor.close()
        
lines = get_static()
insert_static(lines)


def get_dynamic():
    APIKEY = "9aad3ec0edbd53a6fb454f9f7e4ba503dadedd6b"
    NAME = "Dublin"
    STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
    r = requests.get(STATIONS_URI, params={"apiKey": APIKEY,"contract": NAME})
    text = json.loads(r.text)
    return text
    
def update_dynamic(lines):
    db = pymysql.connect("dbbike.cponz0wamutb.eu-west-1.rds.amazonaws.com", "junyi", "db123456", "dbbike")
    cursor = db.cursor()
    for text in lines:
        position = str(text['position']['lat']) + "," + str(text['position']['lng'])
        #sql = "UPDATE dynamic_data SET status = %s, bike_stands = %s ,available_bike_stands = %s ,available_bikes = %s ,last_update = %s  WHERE position = %s"
        value=(text['status'],text['bike_stands'],text['available_bike_stands'],text['available_bikes'],text['last_update'],position)
        sql="insert into dynamic_data(status,bike_stands,available_bike_stands,available_bikes,last_update,position) values (%s,%s,%s,%s,%s,%s)"
        cursor = db.cursor()
        cursor.execute(sql,value)
        db.commit()
        cursor.close()
        
lines = get_dynamic()
print(lines)

update_dynamic(lines)

def get_weather(lat,lng):
    url = "https://api.openweathermap.org/data/2.5/weather?lat=" + lat + "&lon=" + lng + "&appid=dbb2b9eb4f9424b9c2c168ad52c077d9" 
    info = requests.get(url).json()
    return info

def update_weather():
    URI="dbbike.cponz0wamutb.eu-west-1.rds.amazonaws.com"
    PORT="3306"
    DB = "dbbike"
    USER = "junyi"
    PASSWORD = "db123456"
    engine = create_engine("mysql://{}:{}@{}:{}/{}".format(USER,PASSWORD,URI,PORT,DB), echo=True)
    db = pymysql.connect("dbbike.cponz0wamutb.eu-west-1.rds.amazonaws.com", "junyi", "db123456", "dbbike")
    cursor = db.cursor()
    for res in engine.execute("select position,address from static_data;"):
        position = res[0].split(",")
        lat = position[0][1:-1]
        lng = position[1][0:-2]
        address = res[1]
        
        text = get_weather(lat,lng)
        currentDT = datetime.datetime.now()
        #sql = "UPDATE weather SET temperature = %s, wind_speed = %s ,cloudiness = %s ,pressure = %s ,humidity = %s ,time = %s WHERE address = %s"
        #sql="update weather(address,temperature,wind_speed,cloudiness,pressure,humidity,time) values (%s,%s,%s,%s,%s,%s,%s)"
        sql="insert into weather(address,temperature,wind_speed,cloudiness,pressure,humidity,time) values (%s,%s,%s,%s,%s,%s,%s)"
        value=(text['main']['temp'],text['wind']['speed'],text['clouds']['all'],text['main']['pressure'],text['main']['humidity'],currentDT,address)
        cursor = db.cursor()
        cursor.execute(sql,value)
        db.commit()
        cursor.close()

update_weather()