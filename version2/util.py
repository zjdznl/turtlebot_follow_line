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
