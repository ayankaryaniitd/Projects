import cv2

car_cascade= cv2.CascadeClassifier('cars.xml')

img= cv2.imread('Car.jpg')
image= img.copy()
gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cars = car_cascade.detectMultiScale(
    gray,
    scaleFactor=1.03,
    minNeighbors=2,
    minSize=(30,30),
    maxSize=(300,300)
)

for (x,y,xw,yh) in cars:
    cv2.rectangle(image, (x,y),(x+xw,y+yh), (0,255,0), 2)
cv2.imshow('Your image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()