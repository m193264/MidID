#!/usr/bin/env python3
import cgi, cgitb
import json
import base64
import face_recognition
import numpy as np
import scipy.misc
import predict
import re
import io

# Comment out once in production
# cgitb.enable()

############################################################
# Recover POST data
############################################################
data = cgi.FieldStorage()
dataURI = data['postData'].value


############################################################
# Convert base64 img to png file 'capture.png'
############################################################
imgstr = re.search(r'base64,(.*)', dataURI).group(1)
captureFile = open('capture.png','wb')
decoded = base64.b64decode(imgstr)
captureFile.write(decoded)
captureFile.close()

im_arr = scipy.misc.imread('capture.png',mode='RGB')
face_locs = face_recognition.face_locations(im_arr)
face_detected = len(face_locs) > 0

res = {}
if not face_detected:
    res['face_detected'] = False
else:


    handles, probs, names, midsPhotoLink = predict.predict(im_arr)
    res['handles'] = handles
    res['probs'] = probs
    res['names'] = names

    res['face_detected'] = True
    res['mids_img'] = midsPhotoLink
    res['live_img'] = dataURI

# print('Content-type: application/json')
print('Content-type: text/html\n\n')
print(json.dumps(res))
