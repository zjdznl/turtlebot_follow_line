# coding=utf-8
import cv2
import datetime
import numpy as np
import os

import util
from util import show

image = cv2.imread(r'C:\Users\zjdzn\PycharmProjects\ros\input\sample3.jpg')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

s = 100
lower_white = np.array([0,0,255-s])
upper_white = np.array([255, s, 255])

# lower_white = np.array([0, 0, 221])
# upper_white = np.array([180, 30, 255])
mask_white = cv2.inRange(hsv, lower_white, upper_white)
cv2.imshow("before",mask_white)

mask = mask_white
# 中值滤波
mask = cv2.medianBlur(mask, 7)
blur = cv2.GaussianBlur(mask, (5, 5), 0)
util.show(blur, "blur")
mask = cv2.erode(mask, (3,3))

cv2.imshow("after",mask)

# cv2.imwrite("after.jpg", mask)

# To restrict our search to the 100-row portion of
# the image corresponding to about the 0.2m distance in front of the Turtlebot
h, w, d = image.shape #480 640 3
search_top = 2 * h / 5
search_bot = search_top + 100
mask[0:search_top, 0:w] = 0
mask[search_bot:h, 0:w] = 0
mask[:, 0: w / 2 - 150] = 0
mask[:, w / 2 + 150: w] = 0

# To find the line
# Computing the contours of interesting area of hsv image
# https://blog.csdn.net/sunny2038/article/details/12889059
# 轮廓图像
binary, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.imshow("contours",binary)
areas = []

print len(contours)

# 找到轮廓大于阈值的区域
for cont in contours:
    # cv2.contourArea()函数可以计算面积
    area = cv2.contourArea(cont)
    if area > 2700:
        areas.append(area)
    print area

# To find the optimal index of contour
areas.sort()
index = util.findMaxContour(contours)
print len(areas)
cv2.drawContours(image, contours, -1, (0, 0, 255), 3)


cv2.imshow('window', image)



# Computing the centroid of the contours of binary image
# https://www.cnblogs.com/zuochanzi/p/7159108.html
# 图像的距，可以求中心点
M = cv2.moments(contours[index])
signal = True
cx = int(M['m10'] / M['m00'])
cy = int(M['m01'] / M['m00'])
cv2.circle(image, (cx, cy), 20, (255, 0, 0), -1)

util.show(image, "fuck")
# P-controller
err = cx - w / 2
print -float(err) / 45
# twist.linear.x = 0.4
# twist.angular.z = -float(err) / 45


# To find the line
# Computing the contours of interesting area of hsv image
# https://blog.csdn.net/sunny2038/article/details/12889059
# 轮廓图像
# contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# areas = []
#
# print len(contours)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
#
# contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(img, contours, -1, (0,0,255),3)
# cv2.imshow("fuckimg", img)
# cv2.waitKey(0)
cv2.waitKey(0)