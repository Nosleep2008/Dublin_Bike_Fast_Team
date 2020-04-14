'''
Created on Apr 13, 2020

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
from datetime import datetime, timedelta 
import math

def test():
    pass

def bubble_sort(nums):
    for i in range(5):
        for j in range(len(nums) - i - 1):  
            if nums[j][0] > nums[j + 1][0]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]

    return nums

def get_prediction_data(date,time):
    dic_w = {'Clear':1,'Clouds':2,'Mist':3,'Drizzle':4,'Fog':5,'Rain':6,'Snow':7}
    weekday = datetime.strptime(date,"%Y-%m-%d").weekday()
    #day = datetime.strptime(date,"%Y-%m-%d").day
    time = str(time) + ":00:00"
    dic = get_forecast(date + ' ' + time)
    con = dic_w[dic['condition']]
    dic['condition'] = con
    dic['time'] = date + ' ' + time
    dic['weekday'] = weekday
    return dic

def get_forecast(date):
    day = datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
    day_now = datetime.now()
    day = (day - day_now).total_seconds()/3600
    hour = int(day / 3)
    url = 'https://api.openweathermap.org/data/2.5/forecast?lat=53.36&lon=-6.25&appid=dbb2b9eb4f9424b9c2c168ad52c077d9'
    info = requests.get(url).json()
    wind_speed = info['list'][hour]['wind']['speed']
    condition = info['list'][hour]['weather'][0]['main']
    return {'wind':wind_speed,'condition':condition}

def get_old_weather(date):
    dic_w = {'Clear':1,'Clouds':2,'Mist':3,'Drizzle':4,'Fog':5,'Rain':6,'Snow':7}
    date_new = date + timedelta(hours = 8)
    sql = "SELECT * FROM dbike.weather where `datetime` between '"+str(date)+"' and '"+str(date_new)+"';"
    db = pymysql.connect("dbike.cerj203fcxcq.eu-west-1.rds.amazonaws.com", "yuhao", "qwert2008", "dbike")
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    data = cursor.fetchall()
    cursor.close()
    #print(data)
    dic = {}
    dic['condition'] = dic_w[data[0][3]]
    dic['wind'] = data[0][9]
    dic['temp'] = data[0][6]
    return dic

def prediction(number,date,time):
    db = pymysql.connect("dbike.cerj203fcxcq.eu-west-1.rds.amazonaws.com", "yuhao", "qwert2008", "dbike")
    cursor = db.cursor()
    sql="SELECT * FROM dbike.daily_data where `number` = " + str(number) + " group by last_update;"
    cursor.execute(sql)
    db.commit()
    data = cursor.fetchall()
    cursor.close()
    length = len(data)
    i = 0
    dic_pre = get_prediction_data(date,time)
    date_new = datetime.strptime(dic_pre['time'],"%Y-%m-%d %H:%M:%S")
    li = []
    low = datetime.strptime('2020-03-04 09:39:43',"%Y-%m-%d %H:%M:%S")
    high = datetime.strptime('2020-03-24 09:47:28',"%Y-%m-%d %H:%M:%S")
    while i < length:
        date_old = data[i][4]
        #datetime.strptime(str(),"%Y-%m-%d %H:%M:%S")
        if date_old < low or date_old > high:
            i = i + 1
            continue
        available_bike_stands = data[i][2]
        available_bikes = data[i][3]
        weekday_old = date_old.weekday()
        dic_old = get_old_weather(date_old)
        d_condition = float(dic_pre['condition'])-float(dic_old['condition'])
        d_wind = (float(dic_pre['wind']) - float(dic_old['wind']))*5
        if date_new.hour*10000+date_new.minute*100+date_new.second > date_old.hour*10000+date_old.minute*100+date_old.second:
            d_time = (date_new - date_old).seconds/3600
        else:
            d_time = (date_old - date_new).seconds/3600
        d_week = int(dic_pre['weekday'])-int(weekday_old)
        print(d_condition)
        print(d_wind)
        print(d_time)
        print(d_week)
        distance = math.sqrt(d_wind**2 + d_condition**2 + d_time**2 + d_week**2)
        li.append([distance,available_bikes,available_bike_stands])
        #print(li)
        i = i + 1
    bubble_sort(li)  
    weight = 1/li[0][0] + 1/li[1][0] + 1/li[2][0] + 1/li[3][0] + 1/li[4][0]
    prediction_bikes = (li[0][1]*(1/li[0][0]) + li[1][1]*(1/li[1][0]) + li[2][1]*(1/li[2][0]) + li[3][1]*(1/li[3][0]) + li[4][1]*(1/li[4][0]))/ weight
    prediction_stands = (li[0][2]*(1/li[0][0]) + li[1][2]*(1/li[1][0]) + li[2][2]*(1/li[2][0]) + li[3][2]*(1/li[3][0]) + li[4][2]*(1/li[4][0]))/weight
    dic = {}
    dic['prediction_bikes']=prediction_bikes
    dic['prediction_stands']=prediction_stands
    dic['condition'] = dic_pre['condition']
    dic['wind'] = dic_pre['wind']
    dic['temp'] = dic_pre['temp']
    return dic

