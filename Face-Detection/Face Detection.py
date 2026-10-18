import cv2
import numpy as np

face_cascade= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_cascade= cv2.CascadeClassifier('haarcascade_smile.xml')
eye_cascade= cv2.CascadeClassifier('haarcascade_eye.xml')

cap= cv2.VideoCapture(0)

while True:
    ret, frame= cap.read()
    gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face= face_cascade.detectMultiScale(gray, 1.1, 5)

    for (x,y,w,h) in face:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 5)

    for(x,y,w,h) in face:
        roi_gray= gray[y:y+int(1.1*h) , x:x+w]
        smile= smile_cascade.detectMultiScale(roi_gray, 1.7,30)
        eye= eye_cascade.detectMultiScale(roi_gray, 1.5,15)

        if(len(eye)>0):
            cv2.putText(frame, 'Eyes detected', (x,y-30), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255,255,0),5)
        if(len(smile)>0):
            cv2.putText(frame, 'Smile detected', (x,y-60), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255,255,0),5)

    cv2.imshow('Face Detection',frame)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()


# import cv2

# img= (cv2.imread('Photo.jpg')).copy()
# face_cascade= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# faces= face_cascade.detectMultiScale(gray, 1.1, 3)
# for (x,y,xw,yh) in faces:
#     cv2.rectangle(img, (x,y), (x+xw,y+yh), (0,255,0), 2)
# cv2.imshow('Face detector', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()