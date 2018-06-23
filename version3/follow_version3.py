# coding=utf-8

import rospy, cv2, cv_bridge, numpy, math, datetime
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from copy import deepcopy
from util import *
from util import show
import time
import copy
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

kernel = np.ones((5, 5), np.uint8)
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

        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        cv2.imwrite("origin{}.jpg".format(self.i), image)
        img = image
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.GaussianBlur(img, (25, 25), 0)
        edges = cv2.Canny(img, 30, 90)
        edges = cv2.dilate(edges, kernel, iterations=1)


        h, w = img.shape  # 480 640 3
        search_top = 2 * h / 5
        search_bot = search_top + 100
        edges[0:search_top, 0:w] = 0
        edges[search_bot:h, 0:w] = 0
        # edges[:, 0: w / 2 - 150] = 0
        # edges[:, w / 2 + 150: w] = 0

        # show_lines(edges)
        #print r"cut/{}".format(os.path.basename(image))
        cv2.imwrite(r"cut{}.jpg".format(self.i), edges)
        binary, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # cv2.imshow("contours",binary)
        # 记录轮廓面积
        log_contours_area(contours)
        [5069, 5081, 5053, 4754, 4769, 4799, 4699, 4700, 4683, 4717, [7319, 7590], [7231, 7485], [6173, 6441]]

        # 调试，显示轮廓
        back = copy.deepcopy(img)
        cv2.drawContours(back, contours, -1, (0, 0, 255), 3)
        print "len Contours: {}".format(len(contours))
        cv2.imwrite(r"Contours{}.jpg".format(self.i), edges)

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

        # todo 修复其他bug
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
            cv2.circle(drawing, center, 5, (0, 255, 0), -1)
        cv2.imwrite(r"all_center{}.jpg".format(self.i), edges)


        if len(choose_mc):
            if len(choose_mc) == 1:
                cx = choose_mc[0][0]
            else:
                cx = choose_mc[0][0]
            self.err = cx - w / 2

            #todo v
            self.twist.linear.x = 0.3
            self.twist.angular.z = -float(self.err) / 45

            logging.info("x: {}, rotate: {} ".format(self.twist.linear.x, self.twist.angular.z))
            self.cmd_vel_pub.publish(self.twist)

            self.begin = datetime.datetime.now().second
            #todo 要 sleep 吗？
            time.sleep(0.01)
        else:
            print "lose"
            exit(1)
            r = rospy.Rate(2)
            # let's go forward at 0.1 m/s
            # by default angular.z is 0 so setting this isn't required
            move_cmd = Twist()
            move_cmd.linear.x = 0.1

            if self.signal is True:
                if self.err < 0:
                    self.turn_cmd.angular.z = math.radians(-30)
                elif self.err > 0:
                    self.turn_cmd.angular.z = math.radians(30)

                self.cmd_vel_pub.publish(self.turn_cmd)
                now = datetime.datetime.now().second

                # Go forward about 0.2m, then stop
                if math.fabs(now - self.begin) > 2:
                    for x in range(0, 10):
                        self.cmd_vel_pub.publish(move_cmd)
                        r.sleep()
                    self.signal = False



if __name__ == '__main__':
    rospy.init_node('follow')
    follow = Follower()
    rospy.spin()
