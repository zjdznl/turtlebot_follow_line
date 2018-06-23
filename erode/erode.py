# coding=utf-8
import cv2
import numpy as np

from util import show

img = cv2.imread('1024.png', cv2.IMREAD_GRAYSCALE)
assert img is not None
kernel = np.ones((2,2), np.uint8)
erosion = cv2.erode(img, kernel, iterations=1)



def hough_lines(image):
    """
    `image` should be the output of a Canny transform.

    Returns hough lines (not the image with lines)
    """
    return cv2.HoughLinesP(image, rho=1, theta=np.pi / 180, threshold=20, minLineLength=20, maxLineGap=300)


list_of_lines = list(map(hough_lines, erosion))


def draw_lines(image, lines, color=[0, 0, 255], thickness=2, make_copy=True):
    # the lines returned by cv2.HoughLinesP has the shape (-1, 1, 4)
    if make_copy:
        image = np.copy(image)  # don't want to modify the original
    for line in lines:
        try:
            for x1, y1, x2, y2 in line[0]:
                print x1, y1, x2, y2
                cv2.line(image, (x1, y1), (x2, y2), color, thickness)
        except:
            continue
    return image


# print len(draw_lines(erosion, list_of_lines))
line_image = draw_lines(erosion, list_of_lines)
print type(line_image)
show(line_image)
k = cv2.waitKey(0)

cv2.destroyAllWindows()

