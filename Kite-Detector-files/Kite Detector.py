import cv2
import numpy as np

cap= cv2.VideoCapture('Test.mp4')
_, t_i= cap.read()
(h,w)= t_i.shape[:2]
codec= cv2.VideoWriter_fourcc(*'mp4v')
recorder= cv2.VideoWriter('Output.mp4', codec, 30,(w,h))
while True:
    ret, frame= cap.read()
    if not ret:
        break
    if frame is None:
        break
    hsv= cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([35,50,50])
    upper= np.array([90,255,255])

    mask= cv2.inRange(hsv, lower, upper)
    

    kernel = np.ones((5,5), dtype= 'uint8')
    mask= cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask= cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    contours, _= cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area= cv2.contourArea(contour)
        if area > 500:
            (x,y,w,h)= cv2.boundingRect(contour)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
    recorder.write(frame)
    cv2.imshow('The outlined video', frame)
    if( cv2.waitKey(1) & 0xFF == ord('q')):
        break
cap.release()
recorder.release()
cv2.destroyAllWindows()
