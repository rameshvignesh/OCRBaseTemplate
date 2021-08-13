import json
import pytesseract
import cv2
import numpy as np
import sys
import re
import os
from PIL import Image
import ftfy
import pan_read
import aadhar_read
import io
from difflib import SequenceMatcher


unicode:any

pytesseract.pytesseract.tesseract_cmd='C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

#filename = "dl.jpg"
filename = "pan.jpg"
# filename="dummy-pancard.jpg"
img = cv2.imread(filename)
img = cv2.resize(img, None, fx=2, fy=2,interpolation=cv2.INTER_CUBIC)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
var = cv2.Laplacian(img, cv2.CV_64F).var()
# print(var)

if var < 240:
    print("Image is Too Blurry....")
    k= input('Press Enter to Exit.')
    exit(1)


image=Image.open(filename)
text = pytesseract.image_to_string(image, lang = 'eng')

text_output = open('output.txt', 'w', encoding='utf-8')
text_output.write(text)
text_output.close()

file = open('output.txt', 'r', encoding='utf-8')
text = file.read()

text = ftfy.fix_text(text)
text = ftfy.fix_encoding(text)
# print(text)


if "income" in text.lower() or "tax" in text.lower() or "department" in text.lower():
    data = pan_read.pan_read_data(text)
    scanned=True
    
elif "male" in text.lower():
    data = aadhar_read.adhaar_read_data(text)
    scanned=True

else:
    print("Can't Indentify the Document Contents")

try:
    
    to_unicode = unicode
except NameError:
    to_unicode = str
if scanned==True:
    with io.open('info.json', 'w', encoding='utf-8') as outfile:
        data = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
        outfile.write(to_unicode(data))

    with open('info.json', encoding = 'utf-8') as data:
        data_loaded = json.load(data)
else:
    print("Not Properly Scanned. Try Uploading a better quality Image")    

if data_loaded['ID Type'] == 'PAN':
    print("\n---------- PAN Details ----------")
    print("\nPAN Number: ",data_loaded['PAN'])
    print("\nName: ",data_loaded['Name'])
    print("\nFather's Name: ",data_loaded['Father Name'])
    print("\nDate Of Birth: ",data_loaded['Date of Birth'])
    print("\n---------VERIFICATION------------------------")
        
    PAN_Number=  "3WEKY5JOR4FE"
    if SequenceMatcher(None, PAN_Number.lower(), data_loaded['PAN'].lower()).ratio()>0.6:
        print("verified")
    else:
        print("Check the user or upload a high quality image")
    print("\n------------------------------------")

elif data_loaded['ID Type'] == 'Adhaar':
    print("\n---------- ADHAAR Details ----------")
    print("\nADHAAR Number: ",data_loaded['Adhaar Number'])
    print("\nName: ",data_loaded['Name'])
    print("\nDate Of Birth: ",data_loaded['Date of Birth'])
    print("\nSex: ",data_loaded['Sex'])
    print("\n------------------------------------")



k = input("\n\nPress Enter To EXIT")
exit(0)



