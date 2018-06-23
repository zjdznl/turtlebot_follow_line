# coding=utf-8
import numpy as np
import cv2

def show(img, name="default"):
    cv2.imshow(name, img)

def findMaxContour(contours):
    assert len(contours)>0
    max = -1
    max_area = -1
    for index, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max = index
    return max


img = cv2.imread('after.jpg')
# assert img
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY)
show(thresh)
image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# 绘制独立轮廓，如第四个轮廓
# imag = cv2.drawContour(img,contours,-1,(0,255,0),3)
# 但是大多数时候，下面方法更有用
print "contours", len(contours)

max_index = findMaxContour(contours)

imag = cv2.drawContours(img, contours, max_index, (0, 255, 0), 3)


cv2.imshow("fuck", imag)
cv2.waitKey()
