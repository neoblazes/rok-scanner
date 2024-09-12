import cv2
import pytesseract
import os
import sys
from PIL import Image, ImageOps
import csv
import numpy
import re

number = ""
row = [
    'ID','Name','Alliance','Power','Total Killpts','T1 Killpts','T2 Killpts','T3 Killpts','T4 Killpts','T5 Killpts',
    'Highest Power','Victory','Defeat','Dead','Scout Times','Gathered rss','Sent rss','Help times']

if len( sys.argv ) <= 3:
    print("I need 3 args")
    sys.exit()

number = sys.argv[1]
name = sys.argv[2]
filename = sys.argv[3]

def PilThresh(img):
    img = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR + cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return img

def im_crop(rect):
    return im.crop((rect[0] - 40, rect[1] - 40, rect[2] - 40, rect[3] - 40))

with Image.open(os.getcwd() +'\screens\\' + number + 'gov.png') as im:
    powa = im_crop((1078, 437, 1295, 481))
    powa = PilThresh(powa)
    totalkills = im_crop((1353, 437, 1620, 481))
    totalkills = PilThresh(totalkills)
    govid = im_crop((923, 277, 1140, 318))
    govid = PilThresh(govid)
    alliance = im_crop((768, 433, 1082, 474))
    #alliance = PilThresh(alliance)
    alliance = cv2.cvtColor(numpy.array(alliance), cv2.COLOR_RGB2BGR + cv2.COLOR_BGR2GRAY)
    alliance = cv2.bitwise_not(alliance)
    #cv2.imwrite('whatisthis.png', alliance)
power = pytesseract.image_to_string(powa)
power = power.replace('\n', ' ').strip()
power = power.replace(',', '')
power = power.replace('Power ', '')
idstr = pytesseract.image_to_string(govid, config='--psm 6 -c tessedit_char_whitelist=0123456789')
idstr = idstr.replace('\n', ' ').strip()
idstr = idstr.replace(')', '')
allkills = pytesseract.image_to_string(totalkills)
allkills = allkills.replace('\n', ' ').strip()
allkills = allkills.replace(',', '')
allkills = allkills.replace('Kill Points ', '')
alliancestr = pytesseract.image_to_string(alliance, config='--psm 7 --oem 1')
alliancestr = alliancestr.replace('\n', ' ').strip()
if len(alliancestr) < 10:
    alliancestr = "-"

with open(os.getcwd()+'\excel\\'+filename+'.csv', 'a', encoding="utf-8") as csvf:
    wr = csv.DictWriter(csvf, fieldnames=row, lineterminator='\n')
    wr.writerow(
        {'ID': idstr, 'Name': name, 'Alliance': alliancestr, 'Power': power, 'Total Killpts': allkills})

os.remove(os.getcwd() + '\screens\\' + number + 'gov.png')