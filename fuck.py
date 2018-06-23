# coding=utf-8
import cv2
import numpy
import os

# print os.path.exists('sample.jpg')


image = cv2.imread('/home/zjd/PycharmProjects/ROS/img/sample.jpg')
cv2.imshow('image1', image)
image = image.astype(numpy.uint8)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_white = numpy.array([70, 10, 130])
upper_white = numpy.array([180, 110, 255])
mask_white = cv2.inRange(hsv, lower_white, upper_white)

mask = mask_white
mask = cv2.medianBlur(mask, 7)
mask = cv2.erode(mask, (3, 3))

# To restrict our search to the 100-row portion of
# the image corresponding to about the 0.2m distance in front of the Turtlebot
h, w, d = image.shape
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
contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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
index = len(areas) - 1
print len(areas)
cv2.drawContours(image, contours, index, (0, 0, 255), 3)

print "index: ",index

cv2.imshow('window', image)
cv2.waitKey(3)