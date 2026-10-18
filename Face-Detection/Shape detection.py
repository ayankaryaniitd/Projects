import cv2
import numpy as np

image = cv2.imread('Figures.png')
b_g= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(b_g, 140,255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

cont, _= cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.imshow('Originale', image)
for contour in cont:
    if cv2.contourArea(contour)>= cv2.contourArea(cont[0])*0.9:
        continue
    approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
    corners= len(approx)
    match corners:
        case 3:
            shape = 'Triangle'
        case 4:
            shape= 'Rectangle'
        case _:
            shape= 'Ellipse'
    cv2.drawContours(image, [approx], 0, (0,255,0), 5)
    x= approx.ravel()[0]
    y= approx.ravel()[1]
    cv2.putText(image, shape, (x-10,y-10), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0,0,255), 5)
    
cv2.imshow('Outline', image)
cv2.waitKey(0)
cv2.destroyAllWindows()