import cv2
import numpy as np

from util import *


def show_lines(img=r'C:\Users\zjdzn\PycharmProjects\ros\canny\cut\origin27.jpg'):
    img = cv2.imread(img)
    img = cv2.bitwise_not(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = gray
    # edges = cv2.GaussianBlur(gray, (25, 25), 0)
    # edges = cv2.Canny(gray,30,90,apertureSize = 3)
    cv2.imshow('edges', edges)

    minLineLength = 300
    maxLineGap = 40
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 60, minLineLength, maxLineGap)
    print "lines len: {}".format(len(lines))

    # for x in range(0, len(lines)):
    #     for x1,y1,x2,y2 in lines[x]:
    #         cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    #         show(img)
    #         cv2.waitKey(0)

    for x in range(0, len(lines)):
        for x1, y1, x2, y2 in lines[x]:
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow('hough', img)
    cv2.waitKey(0)


if __name__ == '__main__':
    # show_lines()
    files = getinput('cut')
    print len(files)
    for file in files:
        show_lines(file)
