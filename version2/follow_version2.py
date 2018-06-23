# coding=utf-8

import rospy, cv2, cv_bridge, numpy, math, datetime
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from copy import deepcopy
from util import *
from util import show
import time
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')


class Follower:
    def __init__(self):
        self.i = 0
        self.bridge = cv_bridge.CvBridge()
        cv2.namedWindow('window', 1)

        self.image_sub = rospy.Subscriber('/camera/rgb/image_raw', Image, self.image_callback)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)

        self.twist = Twist()
        self.err = 0
        self.turn_cmd = Twist()


        self.signal = False
        self.begin = 0

    def image_callback(self, msg):
        self.i += 1
        logging.info("\n\nnew image call back")

        # opencv格式的图片与ROS中Image-message之间的相互转换
        # To get the image from the camera and convert it to binary image by using opencv
        # bgr8: CV_8UC3, color image with blue-green-red color order
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        print "origin"
        cv2.imwrite("origin{}.jpg".format(self.i), image)

        image = deepcopy(image)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        show(hsv, "hsv")
        cv2.imwrite("hsv{}.jpg".format(self.i), image)


        # 处理图片，对应mask获得二值化，中值滤波和腐蚀效果不大
        mask = get_mask_white(hsv)
        # 中值滤波
        mask = cv2.medianBlur(mask, 9)
        show(mask, "mask")
        #todo delete
        #mask = cv2.erode(mask, (3, 3))
        show(mask, "erode")
        cv2.imwrite("mask{}.jpg".format(self.i), mask)

        # cv2.waitKey(0)

        # 选择区域
        h, w, d = image.shape  # 480 640 3
        search_top = 2 * h / 5
        search_bot = search_top + 100
        #todo cut mask?
        # mask[0:search_top, 0:w] = 0
        # mask[search_bot:h, 0:w] = 0
        # mask[:, 0: w / 2 - 150] = 0
        # mask[:, w / 2 + 150: w] = 0

        # To find the line
        # Computing the contours of interesting area of hsv image
        # https://blog.csdn.net/sunny2038/article/details/12889059
        # 轮廓图像
        binary, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.imshow("contours",binary)

        log_contours_area(contours)
        index = findMaxContour(contours, 2500)
        contours = [contours[i] for i in index]
        logging.info("after filter, has {} contours".format(len(contours)))

        if len(contours):
            max_index = findMaxContour(contours)
            cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
            show(image)

            # Computing the centroid of the contours of binary image
            # https://www.cnblogs.com/zuochanzi/p/7159108.html
            # 图像的距，可以求中心点
            M = cv2.moments(contours[max_index])
            self.signal = True
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.circle(image, (cx, cy), 20, (255, 0, 0), -1)
            cv2.imwrite("point{}.jpg".format(self.i), image)

            # P-controller
            self.err = cx - w / 2
            #todo v
            self.twist.linear.x = 0.2
            self.twist.angular.z = -float(self.err) / 45

            logging.info("x: {}, rotate: {} ".format(self.twist.linear.x, self.twist.angular.z))
            self.cmd_vel_pub.publish(self.twist)

            self.begin = datetime.datetime.now().second
            #todo 要 sleep 吗？
            time.sleep(0.01)
        else:
            # logging.error("filename: {} has 0 contour".format(img_input))
            # show(image)
            # cv2.waitKey(0)

            # Define actions when the point is not be found
            # 5 HZ
            # https: // answers.ros.org / question / 264812 / explanation - of - rospyrate /
            r = rospy.Rate(5)
            # let's go forward at 0.1 m/s
            # by default angular.z is 0 so setting this isn't required
            move_cmd = Twist()
            move_cmd.linear.x = 0.1

            if self.signal is True:
                if self.err < 0:
                    self.turn_cmd.angular.z = math.radians(30)
                elif self.err > 0:
                    self.turn_cmd.angular.z = math.radians(-30)

                self.cmd_vel_pub.publish(self.turn_cmd)
                now = datetime.datetime.now().second

                # Go forward about 0.2m, then stop
                if math.fabs(now - self.begin) > 2:
                    for x in range(0, 10):
                        self.cmd_vel_pub.publish(move_cmd)
                        r.sleep()
                    self.signal = False

        # cv2.imshow('window', image)
        # cv2.waitKey(3)


if __name__ == '__main__':
    rospy.init_node('follow')
    follow = Follower()
    rospy.spin()
