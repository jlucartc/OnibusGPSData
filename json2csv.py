# -*- coding:utf-8 -*-

import json
import re
import base64
import csv

header = [
    'app_id',
    'dev_id',
    'hardware_serial',
    'port',
    'counter',
    'is_retry',
    'payload_raw',
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

filenames = ['data/output20191212_SF9.txt']#,'data/output20191211.txt','data/output20191212_SF9.txt']
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

formatedJSONRows.append(header)

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

                row.append("RETRY")

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

                                row.append("None")
                                row.append("None")
                                row.append("None")
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
                    coords[0] = coords[0].strip()
                    coords[1] = coords[1][:len(coords[1])].strip()
                    coords = coords[0]+" "+coords[1]
                #print(coords)
                row.append(coords)


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

                                row.append("None")
                                row.append("None")
                                row.append("None")
                                row.append("None")
                                


                    else:

                        row.append(message[key][metadataKey])

            else:

                row.append(message[key])

            # == header
            counter = counter + 1

    formatedJSONRows.append(row)

with open('samples_20191212.csv', 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile,delimiter=",")

    for row in formatedJSONRows:

        writer.writerow(row)

csvfile.close()