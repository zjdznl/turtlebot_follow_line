# coding=utf-8
import cv2
import numpy as np
from matplotlib import pyplot as plt
from util import *
import copy

kernel = np.ones((5, 5), np.uint8)


def show_edge(image='origin/origin127.jpg'):
    print "current image: {}".format(image)
    img = cv2.imread(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (25, 25), 0)


    edges = cv2.Canny(img, 30, 90)
    show(edges, "after canny")

    # 膨胀之后白色会变多
    edges = cv2.dilate(edges, kernel, iterations=1)
    show(edges, "dilate")

    # edges = cv2.bitwise_not(edges)
    # show(edges, "invert!!!")

    h, w = img.shape  # 480 640 3
    search_top = 2 * h / 5
    search_bot = search_top + 130
    edges[0:search_top, 0:w] = 0
    edges[search_bot:h, 0:w] = 0
    # edges[:, 0: w / 2 - 150] = 0
    # edges[:, w / 2 + 150: w] = 0

    show(edges, "cut!!")

    # show_lines(edges)

    print "cut/{}".format(os.path.basename(image))
    cv2.imwrite(r"C:\Users\zjdzn\PycharmProjects\ros\canny\cut\{}".format(os.path.basename(image)), edges)

    binary, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.imshow("contours",binary)
    # 记录轮廓面积
    # log_contours_area(contours)
    # [5069, 5081, 5053, 4754, 4769, 4799, 4699, 4700, 4683, 4717, [7319, 7590], [7231, 7485], [6173, 6441]]

    # 调试，显示轮廓
    back = copy.deepcopy(img)
    cv2.drawContours(back, contours, -1, (0, 0, 255), 3)
    print "len Contours: {}".format(len(contours))
    show(back, "fuck Contours")

    # 图像的矩可以帮助我们计算图像的质心，面积等
    mu = []
    for index, contour in enumerate(contours):
        mu.append(cv2.moments(contour, False))

    # 根据这些矩的值，我们可以计算出轮廓的重心：
    # https: // www.kancloud.cn / aollo / aolloopencv / 272892
    mc = []
    # 可供选择的执行 len(contours)>= 4有两个
    # todo 测试有没有bug
    choose_mc = []
    for M in mu:
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = 0, 0
        mc.append((cx, cy))
    print "mc: {}".format(mc)

    #todo 修复其他bug
    x_sum, y_sum, x_avg, y_avg = 0, 0, 0, 0
    if len(contours) == 2:
        for c in mc:
            x_sum += c[0]
            y_sum += c[1]
        x_avg = x_sum / len(mc)
        y_avg = y_sum / len(mc)
        choose_mc.append((x_avg, y_avg))
    elif len(contours) == 4:
        for i in range(0, 4, 2):
            x_sum, y_sum = 0, 0
            for c in mc[i:i + 2]:
                x_sum += c[0]
                y_sum += c[1]
            x_avg = x_sum / 2
            y_avg = y_sum / 2
            choose_mc.append((x_avg, y_avg))
    print "choose mc:{} ".format(choose_mc)

    # 画轮廓及其质心并显示
    drawing = np.zeros(img.shape, np.uint8)
    for index, contour in enumerate(contours):
        color = (255, 0, 0)
        cv2.drawContours(drawing, contours, index, color, 3)
        cv2.circle(drawing, mc[index], 5, (255, 0, 0), -1)

    for center in choose_mc:
        cv2.circle(drawing, center, 5, (255, 0, 0), -1)
    show(drawing, "center")

    # log_contours_area(contours)

    cv2.waitKey(0)


imgs = getinput(r'C:\Users\zjdzn\PycharmProjects\ros\canny\origin')
for img in imgs:
    show_edge(img)
