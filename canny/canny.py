# coding=utf-8
import cv2
import numpy as np
from matplotlib import pyplot as plt
from util import *

kernel = np.ones((5,5),np.uint8)
def show_edge(image = 'origin/origin127.jpg'):
    print "current image: {}".format(image)
    img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    show(img, "gray")
    # cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # g_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # show(g_img)
    img = cv2.GaussianBlur(img, (25, 25), 0)
    show(img, "before canny")
    # edges = cv2.Canny(img, 20, 100)
    edges = cv2.Canny(img, 5, 90)
    show(edges, "after canny")

    # 膨胀之后线条会变粗
    # edges = cv2.dilate(edges,kernel,iterations=1)
    # show(edges,"dilate")

    binary, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow("contours",binary)

    log_contours_area(contours)

    index = findMaxContour(contours, 1)
    contours = [contours[i] for i in index]
    if not len(contours):
        logging.error("filename: {} has 0 contour".format(image))
        show(img)
        cv2.waitKey(0)
        return

    max_index = findMaxContour(contours)
    cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
    show(img)

    # Computing the centroid of the contours of binary image
    # https://www.cnblogs.com/zuochanzi/p/7159108.html
    # 图像的距，可以求中心点
    M = cv2.moments(contours[max_index])
    signal = True
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    cv2.circle(img, (cx, cy), 20, (255, 0, 0), -1)

    show(img)


    cv2.waitKey(0)
    # cv2.waitKey(0)

imgs = getinput(r'C:\Users\zjdzn\PycharmProjects\ros\canny\origin')
for img in imgs:
    show_edge(img)