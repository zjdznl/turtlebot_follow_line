import cv2
import os

assert os.path.exists('img/sample.jpg')

img = cv2.imread('img/sample.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

binary, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, -1, (0,0,255),3)
cv2.imshow("fuckimg", img)
cv2.waitKey(0)