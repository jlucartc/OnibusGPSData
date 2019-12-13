# -*- coding:utf-8 -*-

import json
import re
import base64
import csv
from math import sin, cos, sqrt, atan2, radians

# ---- Distance formula ---- #

gatewayCoordinates = [-3.746569,-38.578127]

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

    return float("{0:.2f}".format(distance*1000)) # returns distance in meters

# ---- Distance formula ---- #

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

filenames = ['data/output20191212_SF9.txt','data/output20191211.txt','data/output20191210.txt']
files = []
fileData = []

for name in filenames:
    
    files.append(open(name,'r'))
    
    if(len(fileData) == 0):
    
        fileData.append(files[len(files)-1].read())
    
    elif(len(fileData) > 0):

        fileData[0] = fileData[0] + files[len(files)-1].read()

data = fileData[0]

# ---- find and replace ---- #

data = re.sub('\w*\/\w*\/\w*\/\w*\s',',',data)
data = json.loads(re.sub('^,','[',data)+"]")

#print(data)

# -------------------------- #

formatedJSONRows = []

#formatedJSONRows.append(header)

for message in data:
    
    row = []

    keys = message.keys()

    #print(keys)

    counter = 0;

    #print(len(keys))

    for key in keys:

        # len(keys) == 8 significa que a mensagem possui campo 'is_retry'

        if(len(keys) == 8):

            if(key == 'payload_raw'):

                row.append(0)
                row.append(0)
                row.append(0)

            elif(key == 'metadata'):

                metadataKeys = message[key].keys()

                #print(metadataKeys)

                for metadataKey in metadataKeys:

                    #print(message[key][metadataKey])

                    if(metadataKey == 'gateways'):

                        for gateway in range(0,len(message[key][metadataKey])):

                            #print(message[key][metadataKey][gateway])

                            gatewayKeys = message[key][metadataKey][gateway].keys()

                            counter = 0

                            for gatewayKey in gatewayKeys:

                                row.append(message[key][metadataKey][gateway][gatewayKey])

                            if(len(gatewayKeys) == 7):

                                row.append(0)
                                row.append(0)
                                row.append(0)
                                row.append("None")

                    else:

                        row.append(message[key][metadataKey])

            else:

                row.append(message[key])

            counter = counter + 1

        else:

            if(counter == 5):

                row.append("False")

                coords = base64.b64decode(message[key]).decode('utf-8')
                coords = coords.split(';')
                #print(coords)
                if(len(coords) > 1):
                    coords[0] = float(coords[0].strip())
                    #print(coords[1][0:len(coords[1])].strip())
                    coords[1] = float(coords[1][0:len(coords[1])-1].strip())
                row.append(coords[0])
                row.append(coords[1])
                row.append(float(getDistance(gatewayCoordinates[0],gatewayCoordinates[1],coords[0],coords[1])))


            elif(key == 'metadata'):

                metadataKeys = message[key].keys()

                #print(metadataKeys)

                for metadataKey in metadataKeys:

                    #print(message[key][metadataKey])

                    if(metadataKey == 'gateways'):

                        for gateway in range(0,len(message[key][metadataKey])):

                            #print(message[key][metadataKey][gateway])

                            gatewayKeys = message[key][metadataKey][gateway].keys()

                            counter = 0

                            for gatewayKey in gatewayKeys:

                                row.append(message[key][metadataKey][gateway][gatewayKey])

                            if(len(gatewayKeys) == 7):

                                row.append(0)
                                row.append(0)
                                row.append(0)
                                row.append("None")
                                


                    else:

                        row.append(message[key][metadataKey])

            else:

                row.append(message[key])

            # == header
            counter = counter + 1

    formatedJSONRows.append(row)

with open('samples.csv', 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile,delimiter=",")

    for row in formatedJSONRows:

        writer.writerow(row)

csvfile.close()