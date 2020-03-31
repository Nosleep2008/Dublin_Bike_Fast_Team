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
from flask import Flask,url_for, g, jsonify,render_template, request
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
    position = request.get_json()
    print(position)
    position = position['position']
    data = get_dynamic(position)
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


if __name__ == "__main__":
    app.run(debug = True)

