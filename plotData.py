# -*- coding:utf-8 -*-

import pandas
import csv
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, sqrt, atan2, radians

# Calcula a distância entre dois pares de coordenadas
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

# Header do arquivo csv
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
    'gtime',
    'channel',
    'rssi',
    'snr',
    'rf_chain',
    'glatitude',
    'glongitude',
    'altitude',
    'location_source'    
]

# Abre arquivo .csv e gera DataFrame
file = open('samples.csv','r')

lists = list(csv.reader(file))

data = pandas.DataFrame(lists,columns=lists[0],dtype=np.array(types))

# Elimina linha de cabeçalho
data = data.drop(0)

# Seta o tipo de dados das colunas que irão ser manipuladas, para evitar erros na hora de filtrar
# os dados.
data.latitude = pandas.to_numeric(data.latitude)
data.longitude = pandas.to_numeric(data.longitude)
data.distancia = pandas.to_numeric(data.distancia)
data.airtime = pandas.to_numeric(data.airtime)
data.rssi = pandas.to_numeric(data.rssi)
data.snr = pandas.to_numeric(data.snr)

# Aplica filtro aos dados, eliminando linhas com coordenadas inválidas
refinedData = data.loc[~((data['latitude'] == 0) & (data['longitude'] == 0))]

# Divide os dados filtrados para cada spreading factor
perSF = refinedData.groupby("data_rate")
sf7 = perSF.get_group('SF8BW125')
sf8 = perSF.get_group('SF7BW125')
sf9 = perSF.get_group('SF9BW125')
sf10 = perSF.get_group('SF10BW125')

# Faz o plot de RSSI versus distância até o gateway para cada spreding factor
sf7.plot(x='distancia',y='rssi',color='red',kind='scatter',legend=True,title="RSSI(dBm) versus distância(m) entre emissor e gateway \n para spreading factor 7 e bandwidth 125kHz")
sf8.plot(x='distancia',y='rssi',color='blue',kind='scatter',legend=True,title="RSSI(dBm) versus distância(m) entre emissor e gateway \n para spreading factor 8 e bandwidth 125kHz")
sf9.plot(x='distancia',y='rssi',color='green',kind='scatter',legend=True,title="RSSI(dBm) versus distância(m) entre emissor e gateway \n para spreading factor 9 e bandwidth 125kHz")
sf10.plot(x='distancia',y='rssi',color='orange',kind='scatter',legend=True,title="RSSI(dBm) versus distância(m) entre emissor e gateway \n para spreading factor 10 e bandwidth 125kHz")


# Faz o plot de SNR versus distância até o gateway para cada spreading factor
sf7.plot(x='distancia',y='snr',color='red',kind='scatter',legend=True,title="SNR(dB) versus distância(m) entre emissor e gateway \n para spreading factor 7 e bandwidth 125kHz")
sf8.plot(x='distancia',y='snr',color='blue',kind='scatter',legend=True,title="SNR(dB) versus distância(m) entre emissor e gateway \n para spreading factor 8 e bandwidth 125kHz")
sf9.plot(x='distancia',y='snr',color='green',kind='scatter',legend=True,title="SNR(dB) versus distância(m) entre emissor e gateway \n para spreading factor 9 e bandwidth 125kHz")
sf10.plot(x='distancia',y='snr',color='orange',kind='scatter',legend=True,title="SNR(dB) versus distância(m) entre emissor e gateway \n para spreading factor 10 e bandwidth 125kHz")


# Ordena os dados de cada spreading factor em ordem descrescente de distância
sf7 = sf7.sort_values(by='distancia',ascending=False)
sf8 = sf8.sort_values(by='distancia',ascending=False)
sf9 = sf9.sort_values(by='distancia',ascending=False)
sf10 = sf10.sort_values(by='distancia',ascending=False)

# Pega a maior distância alcançada em cada spreading factor
maxDistances = []

maxDistances.append([sf7.iloc[0]['distancia'],"SF7BW125"])
maxDistances.append([sf8.iloc[0]['distancia'],"SF8BW125"])
maxDistances.append([sf9.iloc[0]['distancia'],"SF9BW125"])
maxDistances.append([sf10.iloc[0]['distancia'],"SF10BW125"])
maxDistances = pandas.DataFrame(maxDistances,columns=['distancia máxima','Spreading Factor e Bandwidth'])


# Plota o gráfico de distância máxima por spreading factor
maxDistances.plot(y='distancia máxima',x='Spreading Factor e Bandwidth',color='red',kind='bar',legend=True,title="Distância(m) máxima alcançada em cada spreading factor")


# Calcula a média do airtime para cada spreading factor
mAirTime = []
mAirTime.append([sf7.mean()['airtime']/1000000,"SF7BW125"])
mAirTime.append([sf8.mean()['airtime']/1000000,"SF8BW125"])
mAirTime.append([sf9.mean()['airtime']/1000000,"SF9BW125"])
mAirTime.append([sf10.mean()['airtime']/1000000,"SF10BW125"])
mAirTime = pandas.DataFrame(mAirTime,columns=['Airtime médio','Spreading Factor e Bandwidth'])


# Plota a média do airtime para cada spreading factor
mAirTime.plot(y='Airtime médio',x='Spreading Factor e Bandwidth',color='blue',kind='bar',legend=True,title="Airtime médio(ms) em cada spreading factor")

plt.show()

# -------- Algoritmo para selecionar pontos válidos (com 4 ou mais vizinhos) -------- #

# Calcula quais pontos são válidos. Isto é, calcula se um ponto possui ao menos 4 pontos próximos.

#quantidade = refinedData.shape[0]

#aux = [0]*refinedData.shape[0]
#validPoints = []

# Pontos são considerados próximos caso a distância entre eles seja menor do que 2 metros

#raio = 5 

#for i in range(0,quantidade):

#    latSrc = refinedData['latitude'].iloc[i] 
#    longSrc = refinedData['longitude'].iloc[i]

#    for j in range(0,quantidade):

#        latDest = refinedData['latitude'].iloc[j]
#        longDest = refinedData['longitude'].iloc[j]

#        distance = getDistance(latSrc,longSrc,latDest,longDest)

#        if(distance <= raio):

#            if(aux[i] >= 4):

#                validPoints.append(i)

#                aux[i] = -1

#            elif(aux[i] < 4 and aux[i] >= 0):

#                aux[i] = aux[i] + 1

#            else:

#                break

#print(refinedData.iloc[validPoints])

# -------- FIM -------- #