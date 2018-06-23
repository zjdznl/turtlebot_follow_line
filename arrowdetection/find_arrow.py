# coding=utf-8

from copy import deepcopy
from util import *


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
files = getinput('img')


# files = [r'input/sample3.jpg']
for img_input in files:
    logging.info("current file: {}".format(img_input))
    #读取并获得HSV图像
    image = cv2.imread(img_input)
    image = deepcopy(image)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    show(hsv, "hsv")


    #处理图片，对应mask获得二值化，中值滤波和腐蚀效果不大
    mask = get_mask_white(hsv, 50)
    # 中值滤波
    mask = cv2.medianBlur(mask, 9)
    show(mask, "mask")
    mask = cv2.erode(mask, (3,3))
    show(mask, "erode")

    cv2.waitKey(0)

    # 选择区域
    h, w, d = image.shape #480 640 3
    search_top = 2 * h / 5
    search_bot = search_top + 100
    # mask[0:search_top, 0:w] = 0
    # mask[search_bot:h, 0:w] = 0
    # mask[:, 0: w / 2 - 150] = 0
    # mask[:, w / 2 + 150: w] = 0
    #
    # show(mask, "after cut")
    # To find the line
    # Computing the contours of interesting area of hsv image
    # https://blog.csdn.net/sunny2038/article/details/12889059
    # 轮廓图像
    binary, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow("contours",binary)

    log_contours_area(contours)

    index = findMaxContour(contours, 2500)
    contours = [contours[i] for i in index]
    print "after"
    log_contours_area(contours)
    if not len(contours):
        logging.error("filename: {} has 0 contour".format(img_input))
        show(image)
        cv2.waitKey(0)
        continue

    max_index = findMaxContour(contours)
    # cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
    #add every area
    for i in range(len(contours)):
        print "draw {} image contour, area is {}".format(i, cv2.contourArea(contours[i]))
        cv2.drawContours(image, contours, i, (0, 0, 255), 3)
        show(image)
        cv2.waitKey(0)

    show(image)

    # Computing the centroid of the contours of binary image
    # https://www.cnblogs.com/zuochanzi/p/7159108.html
    # 图像的距，可以求中心点
    M = cv2.moments(contours[max_index])
    signal = True
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    cv2.circle(image, (cx, cy), 20, (255, 0, 0), -1)

    show(image)
    cv2.imwrite(os.path.join('output', os.path.basename(img_input)), image)
    cv2.waitKey(0)