'''
Created on Mar 24, 2020

@author: Haniel Wang
'''

from datetime import datetime
st = "2020-03-07 12:52:58"
week = datetime.strptime(st,"%Y-%m-%d %H:%M:%S").weekday()
h = datetime.strptime(st,"%Y-%m-%d %H:%M:%S").hour
print(h)

