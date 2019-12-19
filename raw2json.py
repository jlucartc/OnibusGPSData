# -*- coding:utf-8 -*-

import re

import os

#searchString = "./data/RAW/*"

pathPreffixSrc = "data/RAW/"

pathPreffixDest = "data/JSON/"

filenames = os.listdir(pathPreffixSrc)

print(filenames)

for name in filenames:

	src = open(pathPreffixSrc+name,'r')

	fileData = src.read()

	src.close()

	fileData = re.sub('\w*\/\w*\/\w*\/\w*\s',',',fileData)

	fileData = "["+re.sub('^,','',fileData)+"]"

	dest = open(pathPreffixDest+name,'w')

	dest.write(fileData)

	dest.close()