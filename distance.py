# -*- coding:utf-8 -*-

import json
import re
import base64
import csv
from math import sin, cos, sqrt, atan2, radians

def getDistance(latSource,longSource,latDest,longDest):

    R = 6373.0

    lat1 = radians(latSource)
    lon1 = radians(longSource)
    lat2 = radians(latDest)
    lon2 = radians(longDest)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance*1000 # returns distance in meters

print(getDistance(-3.746575,-38.578132,-3.747929,-38.576292)*1000)

