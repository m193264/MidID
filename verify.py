#!/usr/bin/env python3
import cgi, cgitb
import json
from datetime import datetime
import base64
import os
import re
import csv

def addStats(timestr, handle, fname, degree, negDegree, negHandle):
    stats_fname = 'l2_stats.csv'
    full_path = 'stats/'+stats_fname

    first = True
    if os.path.exists(full_path):
        first = False

    stats_csv = open(full_path, 'a')
    csv_writer = csv.writer(stats_csv)
    if first:
        # potentially could add timestr as first field
        csv_writer.writerow(['Handle', 'File', 'Degree', 'Negative Degree', 'Negative Handle'])
    csv_writer.writerow([handle, fname, degree, negDegree, negHandle])
    stats_csv.close()


##########################################################################
# Recover POST data
##########################################################################
data = cgi.FieldStorage()
handle = data['handle'].value
dataURI = data['live-img'].value
degree = data['degree'].value
negDegree = data['negDegree'].value
negHandle = data['negHandle'].value


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
addStats(timestr, handle, fname, degree, negDegree, negHandle)

res = {}
res['verified'] = True
res['time'] = timestr
print('Content-type: text/html\n\n')
print(json.dumps(res))
