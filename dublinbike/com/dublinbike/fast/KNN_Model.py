'''
Created on Apr 13, 2020

@author: Haniel Wang, CHEN PENG, Junyi ZHANG
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



def bubble_sort(nums):
    for i in range(len(nums)):
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
    temp = info['list'][hour]['main']['temp']
    return {'wind':wind_speed,'condition':condition,'temp':temp}

def get_csv():
    low = '2020-03-04 09:39:43'
    high = '2020-03-24 09:47:28'
    sql = "SELECT * FROM dbike.weather where `datetime` between '"+ low +"' and '"+ high +"';"
    conn = pymysql.connect("dbike.cerj203fcxcq.eu-west-1.rds.amazonaws.com", "yuhao", "qwert2008", "dbike")
    df = pd.read_sql(sql, con=conn)
    df.to_csv("old_weather.csv",index=False)
    
def get_old_weather(low,df):
    dic_old_weather = {}
    dic_w = {'Clear':1,'Clouds':2,'Mist':3,'Drizzle':4,'Fog':5,'Rain':6,'Snow':7}
    #low = datetime.strptime(low,"%Y-%m-%d %H:%M:%S")
    high = low + timedelta(hours = 8)
    #low = '2020-03-04 15:20:02'
    #high = '2020-03-04 15:40:02'
    temp=df[(df['datetime']>=low) & (df['datetime']<=high)]
    #temp.head(100)
    if temp.empty:
        return dic_old_weather
    temp.iloc[[0],[3]].values[0][0]
    #print(data)
    dic_old_weather['condition'] = dic_w[temp.iloc[[0],[3]].values[0][0]]
    dic_old_weather['wind'] = temp.iloc[[0],[9]].values[0][0]
    dic_old_weather['temp'] = temp.iloc[[0],[6]].values[0][0]
    return dic_old_weather

def prediction(number,date,time):
    get_csv()
    db = pymysql.connect("dbike.cerj203fcxcq.eu-west-1.rds.amazonaws.com", "yuhao", "qwert2008", "dbike")
    cursor = db.cursor()
    sql="SELECT * FROM dbike.daily_data where `number` = " + str(number) + " group by last_update;"
    cursor.execute(sql)
    db.commit()
    data = cursor.fetchall()
    cursor.close()
    length = len(data)
    i = 0
    count = 0
    dic_pre = get_prediction_data(date,time)
    date_new = datetime.strptime(dic_pre['time'],"%Y-%m-%d %H:%M:%S")
    li = []
    print(length)
    df = pd.read_csv('old_weather.csv')
    df['datetime'] = df['datetime'].astype('datetime64')
    while i < length:
        date_old = data[i][4]
        available_bike_stands = data[i][2]
        available_bikes = data[i][3]
        weekday_old = date_old.weekday()
        dic_old = get_old_weather(date_old,df)
        i = i + 1
        if count == 5:
            break
        if not dic_old:
            continue
        d_condition = float(dic_pre['condition'])-float(dic_old['condition'])
        d_wind = (float(dic_pre['wind']) - float(dic_old['wind']))*5
        if date_new.hour*10000+date_new.minute*100+date_new.second > date_old.hour*10000+date_old.minute*100+date_old.second:
            d_time = (date_new - date_old).seconds/3600
        else:
            d_time = (date_old - date_new).seconds/3600
        d_week = int(dic_pre['weekday'])-int(weekday_old)
        d_time = round(d_time,3)
        #print(d_condition)
        #print(d_wind)
        #print(d_time,end=" ")
        #print(d_week)
        distance = math.sqrt(d_wind**2 + d_condition**2 + d_time**2 + d_week**2)
        li.append([distance,available_bikes,available_bike_stands])
        #print(li)
    print(len(li))
    bubble_sort(li)
    print(li[0],li[1],li[2])
    weight = 1/li[0][0] + 1/li[1][0] + 1/li[2][0] + 1/li[3][0] + 1/li[4][0]
    prediction_bikes = (int(li[0][1])*(1/li[0][0]) + int(li[1][1])*(1/li[1][0]) + int(li[2][1])*(1/li[2][0]) + int(li[3][1])*(1/li[3][0]) + int(li[4][1])*(1/li[4][0]))/ weight
    prediction_stands = (int(li[0][2])*(1/li[0][0]) + int(li[1][2])*(1/li[1][0]) + int(li[2][2])*(1/li[2][0]) + int(li[3][2])*(1/li[3][0]) + int(li[4][2])*(1/li[4][0]))/weight
    dic = {}
    dic_w = {'1':'Clear','2':'Clouds','3':'Mist','4':'Drizzle','5':'Fog','6':'Rain','7':'Snow'}
    dic['prediction_bikes']=int(prediction_bikes)
    dic['prediction_stands']=int(prediction_stands)
    dic['condition'] = dic_w[str(dic_pre['condition'])]
    dic['wind'] = dic_pre['wind']
    dic['temp'] = str(dic_pre['temp']) + 'K'
    return dic



#print(prediction(32,'2020-04-12','09'))