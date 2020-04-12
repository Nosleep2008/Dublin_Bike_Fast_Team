'''
Created on Apr 4, 2020

@author: Haniel Wang
'''
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

def weather():
    db_mohan = pymysql.connect("bikesdata.cnqobaauuxez.us-east-1.rds.amazonaws.com", "admin", "rootadmin", "dbikes")
    cursor_mohan = db_mohan.cursor()
    db_yuhao = pymysql.connect("dbike.cerj203fcxcq.eu-west-1.rds.amazonaws.com", "yuhao", "qwert2008", "dbike")
    cursor_yuhao = db_yuhao.cursor()
    sql="select coord_lon,coord_lat,weather_id,weather_main,weather_description,weather_icon,main_temp,main_pressure,main_humidity,wind_speed,wind_deg,clouds_all,dt,sys_sunrise,sys_sunset from Weather"
    sql2="insert into weather(longitude,latitude,weather_id,weather_main,weather_description,weather_icon,temperature,pressure,humidity,wind_speed,wind_degree,clouds_all,datetime,sunrise,sunset) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor_mohan.execute(sql)
    data2 = cursor_mohan.fetchall()
    cursor_yuhao.executemany(sql2, data2)
    db_yuhao.commit()
    db_mohan.close()
    print("finished!")  


def weekly():
    db_mohan = pymysql.connect("bikesdata.cnqobaauuxez.us-east-1.rds.amazonaws.com", "admin", "rootadmin", "dbikes")
    cursor_mohan = db_mohan.cursor()
    db_yuhao = pymysql.connect("dbike.cerj203fcxcq.eu-west-1.rds.amazonaws.com", "yuhao", "qwert2008", "dbike")
    cursor_yuhao = db_yuhao.cursor()
    sql="select status,bike_stands,available_bike_stands,available_bikes,last_update,number from bikes_available"
    sql2="insert into weekly_data(status,bike_stands,available_bike_stands,available_bikes,last_update,number) values (%s,%s,%s,%s,%s,%s)"
    cursor_mohan.execute(sql)
    data2 = cursor_mohan.fetchall()
    cursor_yuhao.executemany(sql2, data2)
    db_yuhao.commit()
    db_mohan.close()
    print("finished!")  

def daily():
    db_mohan = pymysql.connect("bikesdata.cnqobaauuxez.us-east-1.rds.amazonaws.com", "admin", "rootadmin", "dbikes")
    cursor_mohan = db_mohan.cursor()
    db_yuhao = pymysql.connect("dbike.cerj203fcxcq.eu-west-1.rds.amazonaws.com", "yuhao", "qwert2008", "dbike")
    cursor_yuhao = db_yuhao.cursor()
    sql="select status,bike_stands,available_bike_stands,available_bikes,last_update,number from Bike"
    sql2="insert into daily_data(status,bike_stands,available_bike_stands,available_bikes,last_update,number) values (%s,%s,%s,%s,%s,%s)"
    cursor_mohan.execute(sql)
    data2 = cursor_mohan.fetchall()
    cursor_yuhao.executemany(sql2, data2)
    db_yuhao.commit()
    db_mohan.close()
    print("finished!")  

daily()
#weekly()

#weather()
