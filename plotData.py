# -*- coding:utf-8 -*-

import pandas
import csv
import numpy as np

header = [
    'app_id',
    'dev_id',
    'hardware_serial',
    'port',
    'counter',
    'is_retry',
    'latitude',
    'longitude',
    'distancia',
    'time',
    'frequency',
    'modulation',
    'data_rate',
    'airtime',
    'coding_rate',
    'gtw_id',
    'timestamp',
    'time',
    'channel',
    'rssi',
    'snr',
    'rf_chain',
    'latitude',
    'longitude',
    'altitude',
    'location_source'    
]

types = [str,str,str,int,int,str,float,float,float,str,str,str,str,int,str,str,int,str,int,int,float,int,float,float,int,str]

file = open('samples.csv','r')

lists = list(csv.reader(file))

#print(lists)

data = pandas.DataFrame(lists,columns=header,dtype=np.array(types))

data.distancia.apply(str)

print(data.query("distancia>'1000.0'")['distancia'])
#print(data)


# group by data rate