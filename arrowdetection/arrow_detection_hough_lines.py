import cv2, numpy as np, argparse

import util


def left_or_right(image):
    img = cv2.imread(image)
    # convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # apply canny edge detection to the image
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    # show what the image looks like after the application of previous functions
    # cv2.imshow("canny'd image", edges)
    # perform HoughLines on the image
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 20)
    # create an array for each direction, where array[0] indicates one of the lines and array[1] indicates the other, which if both > 0 will tell us the orientation
    left = [0, 0]
    right = [0, 0]
    # iterate through the lines that the houghlines function returned
    for object in lines:
        theta = object[0][1]
        rho = object[0][0]
        # cases for right/left arrows
        if ((np.round(theta, 2)) >= 1.0 and (np.round(theta, 2)) <= 1.1) or (
                        (np.round(theta, 2)) >= 2.0 and (np.round(theta, 2)) <= 2.1):
            if (rho >= 20 and rho <= 30):
                left[0] += 1
            elif (rho >= 60 and rho <= 65):
                left[1] += 1
            elif (rho >= -73 and rho <= -57):
                right[0] += 1
            elif (rho >= 148 and rho <= 176):
                right[1] += 1

    result_list = [0, 0]
    result = 0

    print "image name:{} , left and right: {}".format(image, (left, right))
    if left[0] >= 1 and left[1] >= 1:
        result_list[0] = 1
    if right[0] >= 1 and right[1] >= 1:
        result_list[1] = 1

    if result_list[0] and result_list[1]:
        if sum(right) > sum(left):
            result = 1
        else:
            result = -1
    elif result_list[0]:
        result = -1
    else:
        result = 1

    return result



    # print(left, right)


image_list = util.getinput('img')
print image_list
for image in image_list:
    print left_or_right(image)
