'''
Created on Mar 24, 2020

@author: Haniel Wang
'''
from datetime import datetime
st = "2020-03-07 12:52:58"
week = datetime.strptime(st,"%Y-%m-%d %H:%M:%S").weekday()
h = datetime.strptime(st,"%Y-%m-%d %H:%M:%S").hour
print(h)
'''
a = ((1,2,3),(1,4),(5,6,7,8))
print(len(a))


dic = {'0':[1,2],'1':[],'2':[],'3':[],'4':[],'5':[],'6':[]}
print(dic['0'])
a = 111
b= 222
dic['0'] = [a,b]
print(dic['0'])
'''