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
from datetime import datetime
from flask import Flask,url_for, g, jsonify,render_template, request
from _operator import length_hint
app = Flask(__name__)
'''
Created on Mar 24, 2020

@author: Haniel Wang
'''
avali = {}


@app.route('/')   
def index():
    print("hello")
    stations = get_static().get_json()
    print("hello")
    print(stations)
    return render_template('index.html',station="123" ,map_key="AIzaSyDFJziVkEvhTBxI1JZ_sznFA_Kbm7FWLAM")

@app.route('/hello')   
def hello():
    return render_template('hello.html')

@app.route('/map')   
def map():
    stations = get_static().get_json()
    return render_template('map.html',stations = stations)

@app.route('/check_rest',methods=['POST'])
def check_rest():
    recieve_data = request.get_json()
    print(recieve_data)
    position = recieve_data['position']
    data = get_dynamic(position)
    return data

@app.route('/check_weekly',methods=['POST'])
def check_weekly():
    recieve_data = request.get_json()
    print(recieve_data)
    number = recieve_data['number']
    data = get_weekly(number)
    return data


@app.route('/check_daily',methods=['POST'])
def check_daily():
    recieve_data = request.get_json()
    print(recieve_data)
    number = recieve_data['number']
    data = get_daily(number)
    return data

def get_static():
    db = pymysql.connect("dbbike.cponz0wamutb.eu-west-1.rds.amazonaws.com", "junyi", "db123456", "dbbike")
    cursor = db.cursor()
    sql="SELECT * FROM static_data"
    cursor.execute(sql)
    db.commit()
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

def get_dynamic(position):
    db = pymysql.connect("dbbike.cponz0wamutb.eu-west-1.rds.amazonaws.com", "junyi", "db123456", "dbbike")
    cursor = db.cursor()
    sql="SELECT * FROM dynamic_data where position='" + position +"'"
    cursor.execute(sql)
    db.commit()
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

def get_weekly(number):
    db = pymysql.connect("dbike.cerj203fcxcq.eu-west-1.rds.amazonaws.com", "yuhao", "qwert2008", "dbike")
    cursor = db.cursor()
    sql="SELECT * FROM dbike.daily_data where `number` = " + str(number) + " group by last_update;"
    cursor.execute(sql)
    db.commit()
    data = cursor.fetchall()
    cursor.close()
    length = len(data)
    dic_stand = {'0':[],'1':[],'2':[],'3':[],'4':[],'5':[],'6':[]}
    dic_bike = {'0':[],'1':[],'2':[],'3':[],'4':[],'5':[],'6':[]}
    dic = {'0':[],'1':[],'2':[],'3':[],'4':[],'5':[],'6':[]}
    i = 0
    while i < length:
        time = data[i][4]
        available_bike_stands = data[i][2]
        available_bikes = data[i][3]
        week = time.weekday()
        dic_stand[str(week)].append(available_bike_stands)
        dic_bike[str(week)].append(available_bikes)
        i = i + 1
        
    for i in range(0,7):
        dic_stand[str(i)] = Get_Average(dic_stand[str(i)])
        print(dic_stand[str(i)])
        dic_bike[str(i)] = Get_Average(dic_bike[str(i)])
        print(dic_bike[str(i)])
        dic[str(i)] = [dic_stand[str(i)], dic_bike[str(i)]]
    return jsonify(dic)

def get_daily(number):
    db = pymysql.connect("dbike.cerj203fcxcq.eu-west-1.rds.amazonaws.com", "yuhao", "qwert2008", "dbike")
    cursor = db.cursor()
    sql="SELECT * FROM dbike.daily_data where `number` = " + str(number) + " group by last_update;"
    cursor.execute(sql)
    db.commit()
    data = cursor.fetchall()
    cursor.close()
    length = len(data)
    dic_stand = {'0':[],'1':[],'2':[],'3':[],'4':[],'5':[],'6':[],'7':[],'8':[],'9':[],'10':[],'11':[],'12':[],'13':[],'14':[],'15':[],'16':[],'17':[],'18':[],'19':[],'20':[],'21':[],'22':[],'23':[]}
    dic_bike = {'0':[],'1':[],'2':[],'3':[],'4':[],'5':[],'6':[],'7':[],'8':[],'9':[],'10':[],'11':[],'12':[],'13':[],'14':[],'15':[],'16':[],'17':[],'18':[],'19':[],'20':[],'21':[],'22':[],'23':[]}
    dic = {'0':[],'1':[],'2':[],'3':[],'4':[],'5':[],'6':[],'7':[],'8':[],'9':[],'10':[],'11':[],'12':[],'13':[],'14':[],'15':[],'16':[],'17':[],'18':[],'19':[],'20':[],'21':[],'22':[],'23':[]}
    i = 0
    while i < length:
        time = data[i][4]
        available_bike_stands = data[i][2]
        available_bikes = data[i][3]
        hour = time.hour
        dic_stand[str(hour)].append(available_bike_stands)
        dic_bike[str(hour)].append(available_bikes)
        i = i + 1
        
    for i in range(0,24):
        dic_stand[str(i)] = Get_Average(dic_stand[str(i)])
        print(dic_stand[str(i)])
        dic_bike[str(i)] = Get_Average(dic_bike[str(i)])
        print(dic_bike[str(i)])
        dic[str(i)] = [dic_stand[str(i)], dic_bike[str(i)]]
    return jsonify(dic)


def Get_Average(li):
    s = 0
    for item in li:     
        s += int(item)  
    return s/len(li)        


if __name__ == "__main__":
    app.run(debug = True)

