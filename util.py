# coding=utf-8
import logging
logging.basicConfig(level=logging.INFO)
import numpy as np
import cv2
import os


def findMaxContour(contours, threshold=0):
    #如果指定 threshold 返回大于其的list， 否则返回最大 contours 的index
    # assert len(contours)>0
    max = -1
    max_list = []
    max_area = -1
    for index, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max = index
        if area>threshold:
            max_list.append(index)
    if threshold:
        return max_list
    else:
        return max

def show_lines(img):
    '''
    传入一个照片，画线
    :param image:
    :return:
    '''
    gray = img

    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    binary, contours, hier = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for index, cnt in enumerate(contours):
        # then apply fitline() function
        [vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)

        # Now find two extreme points on the line to draw line
        lefty = int((-x * vy / vx) + y)
        righty = int(((gray.shape[1] - x) * vy / vx) + y)

        # Finally draw the line
        cv2.line(img, (gray.shape[1] - 1, righty), (0, lefty), 255, 2)
        cv2.imshow('img{}'.format(index), img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def get_lines_center():
    pass
    # # ===begin
    # cut_back = cv2.imread(edges)
    # cut_back = cv2.bitwise_not(cut_back)
    # gray = cv2.cvtColor(cut_back, cv2.COLOR_BGR2GRAY)
    # edges = gray
    # # edges = cv2.GaussianBlur(gray, (25, 25), 0)
    # # edges = cv2.Canny(gray,30,90,apertureSize = 3)
    # cv2.imshow('edges', edges)
    #
    # minLineLength = 300
    # maxLineGap = 40
    # lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 60, minLineLength, maxLineGap)
    # print "lines len: {}".format(len(lines))
    #
    # for x in range(0, len(lines)):
    #     for x1, y1, x2, y2 in lines[x]:
    #         cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    #
    # cv2.imshow('hough', img)
    # pass


def show(img, name="default"):
    cv2.imshow(name, img)
    pass

def getinput(filepath='input'):
    file_list = []
    for (root, dirs, files) in os.walk(filepath):
        for filename in files:
            file_list.append(os.path.join(root, filename))

    return file_list

def log_contours_area(contours):
    areas = []
    for contour in contours:
        areas.append(cv2.contourArea(contour))

    logging.info(areas)

def get_mask_white(hsv, s=100):
    lower_white = np.array([0,0,255-s])
    upper_white = np.array([180, s, 255])
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    return mask_white



if __name__ == '__main__':
    getinput()
