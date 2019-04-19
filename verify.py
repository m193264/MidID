#!/usr/bin/env python3
import cgi, cgitb
import json
from datetime import datetime
import base64
import os
import re
import csv

def addStats(handle, fname, degree):
    stats_fname = 'l2_stats.csv'
    full_path = 'stats/'+stats_fname

    first = True
    if os.path.exists(full_path):
        first = False

    stats_csv = open(full_path, 'a')
    csv_writer = csv.writer(stats_csv)
    if first:
        csv_writer.writerow(['Handle', 'File', 'Degree'])
    csv_writer.writerow([handle, fname, degree])
    stats_csv.close()


##########################################################################
# Recover POST data
##########################################################################
data = cgi.FieldStorage()
handle = data['handle'].value
dataURI = data['live-img'].value
degree = data['degree'].value


##########################################################################
# Save verified image
##########################################################################
directory = 'imgs/live-imgs/raw/' + handle
timestr = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S-%f')
fname = directory + '/' + handle + '_' + timestr + '.png'
if not os.path.exists(directory):
    os.makedirs(directory)
live_img_file = open(fname, 'wb')
imgstr = re.search(r'base64,(.*)', dataURI).group(1)
decoded = base64.b64decode(imgstr)
live_img_file.write(decoded)
live_img_file.close()
addStats(handle, fname, degree)

res = {}
res['verified'] = True
res['time'] = timestr
print('Content-type: text/html\n\n')
print(json.dumps(res))
