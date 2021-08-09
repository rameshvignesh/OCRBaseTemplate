import cv2
from numpy import string_
import pytesseract
from difflib import SequenceMatcher

pytesseract.pytesseract.tesseract_cmd='C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
def scan():
            # img =cv2.imread(r'E:\LTI\Salvathon\Trial\A_sample_of_Aadhaar_card.jpg')
            img =cv2.imread(r'E:\LTI\Salvathon\Trial\New Doc 2019-08-29 22.56.09_31.jpg')

            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            # print(pytesseract.image_to_string(img))

            name='Ramesh'
            # name='DoB'
            verification=[]
            # print(img.shape)
            hImg,wImg,pixel=img.shape
            boxes=pytesseract.image_to_data(img)
            for b in boxes.splitlines():
                        b=b.split() 
                        if len(b)==12:
                            # print(b) 
                            if b[6]!='left' and b[7]!='top' and b[8]!='width'  and b[9]!='height' :
                                x,y,w,h=int(b[6]),int(b[7]),int(b[8]),int(b[9])
                                cv2.rectangle(img,(x,y),(w+x,h+y),(0,0,255,3))
                                cv2.putText(img,b[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)
                                # cv2.putText(img,b[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,0.4,(50,50,255),1)
                            if b[4] in ('2','3','4'):
                            # if b[4] in ('1','2'):
                                if SequenceMatcher(None, name.lower(), b[11].lower()).ratio()>0.6:
                                    verification.append(b[11].lower())
                                    
            print(verification)                  
            if len(verification)>=1:
                print('verified')
            else:
                print('check the document quality and upload it again')

            imS = cv2.resize(img,(960, 540))              
            cv2.imshow('Aadhar',imS)
            cv2.waitKey(0)



if __name__ == "__main__":
    scan()


