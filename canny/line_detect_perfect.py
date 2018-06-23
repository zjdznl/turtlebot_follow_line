# Load image, convert to grayscale, threshold and find contours
import cv2

img = cv2.imread(r'C:\Users\zjdzn\PycharmProjects\ros\canny\cut\origin71.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
binary, contours,hier = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    # then apply fitline() function
    [vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)

    # Now find two extreme points on the line to draw line
    lefty = int((-x * vy / vx) + y)
    righty = int(((gray.shape[1] - x) * vy / vx) + y)

    # Finally draw the line
    cv2.line(img, (gray.shape[1] - 1, righty), (0, lefty), 255, 2)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()