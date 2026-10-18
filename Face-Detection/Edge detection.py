import cv2

image = cv2.imread('images.jpeg',0)
# outline = cv2.Canny(image, 119,120)
cv2.imshow('Original', image)
# cv2.imshow('Outlines', outline)
ret, thre= cv2.threshold(image, 40, 255, cv2.THRESH_BINARY)
cv2.imshow('Thresholded image', thre)
cv2.waitKey(0)
cv2.destroyAllWindows()