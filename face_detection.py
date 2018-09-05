import cv2 #opencv
from pygame import mixer #run .mp3
import serial #pyserial

conexao = serial.Serial('COM3', 9600)

mixer.init()

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

positive = 0
negative = 0
ant = [0,0]
while True:
    
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
    
    if len(faces) > 0:
        negative = 0
        positive = positive + 1
        
        if positive > 10:
            positive = 0
            ant[0] = ant[1]
            ant[1] = 1
            
            if ant[0] != ant[1]:
                conexao.write(b'1')

                print("Oi!!")
                
                mixer.music.load('ola.mp3')
                mixer.music.play()
                
                

    else:
        positive = 0
        negative = negative + 1
        
        if negative > 20:
            negative = 0
            ant[0] = ant[1]
            ant[1] = 0
            
            if ant[0] != ant[1]:
                conexao.write(b'0')
                
                print("Tchau!!")
                           
                mixer.music.load('tchau.mp3')
                mixer.music.play()
                #os.system("%systemroot%\system32\scrnsave.scr /s")
            
    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

conexao.write(b'0')

cap.release()
cv2.destroyAllWindows()