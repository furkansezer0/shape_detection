import cv2
import numpy as np
import math


class ShapeDetection:
    def __init__(self):
        self.img = cv2.imread('shapes.png')
        self.width = self.img.shape[1]
        self.height = self.img.shape[0]
        self.contours = None
        self.corner_counter = 0
        self.sp_x = None
        self.sp_y = None
        self.tp_x = None
        self.tp_y = None
        self.ep_x = None
        self.ep_y = None
        self.max_ind = 0
        self.min_ind = 0
        self.change = False
    def __call__(self):
        self.filter_image(self.img)
        self.general()

    def filter_image(self, img):
        mask = np.zeros((img.shape[0], img.shape[1], 1), np.uint8)
        # converting image into grayscale image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # setting threshold of gray image
        _, threshold = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)

        self.contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    def dist_betw_two_poi(self, x1: int, x2: int, y1: int, y2: int):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def dist_betw_line_poi(self, a: int, b: int, c: int, x1: int, y1: int):
        distance = (abs(a * x1 + b * y1 + c)) / math.sqrt(a ** 2 + b ** 2)
        return distance

    def arc_length_finder(self, img, contour):
        arc_length = 0
        for c in range(len(contour)):
            if c != len(contour) - 1:
                current_c = contour[c]
                next_c = contour[c + 1]
                if c == 0 or c == len(contour) - 2:
                    cv2.circle(img, (current_c[0][0], current_c[0][1]), 1, color=(0, 255, 0), thickness=1)
                arc_length += self.dist_betw_two_poi(current_c[0][0], next_c[0][0], current_c[0][1], next_c[0][1])
        arc_length += 1
        return arc_length

    def general(self):
        for contour in self.contours:
            # print(arc_length_finder(contour))
            # print(cv2.arcLength(contour, True))
            self.corner_counter = 0
            self.main(contour)
        # print(self.corner_counter)


    def main(self, contour):
        sp_x, sp_y = self.sp_x, self.sp_y
        sp_x, sp_y = contour[0][0][0], contour[0][0][1]
        max_dis = 0
        short_dis = 0
        max_ind = self.max_ind
        min_ind = self.min_ind
        short_ind = 0
        for c in range(0, len(contour)):
            tp_x, tp_y = contour[c][0][0], contour[c][0][1]
            if self.dist_betw_two_poi(sp_x, tp_x, sp_y, tp_y) >= max_dis:
                max_dis = self.dist_betw_two_poi(sp_x, tp_x, sp_y, tp_y)
                max_ind = c

        min_ind = 0
        ep_x, ep_y = contour[max_ind][0][0], contour[max_ind][0][1]
        # print(self.arc_length_finder(self.img, contour))
        ccw_counter = self.shape_detection(contour, epsilon=self.arc_length_finder(self.img, contour)*0.005, sp_x=sp_x, sp_y=sp_y, ep_x=ep_x, ep_y=ep_y, max_ind=max_ind, min_ind=min_ind)
        min_ind = max_ind
        max_ind = len(contour) - 1
        sp_x, sp_y = contour[min_ind][0][0], contour[min_ind][0][1]
        ep_x, ep_y = contour[max_ind][0][0], contour[max_ind][0][1]
        ccw_cw_counter = self.shape_detection(contour, epsilon=self.arc_length_finder(self.img, contour)*0.005, sp_x=sp_x, sp_y=sp_y, ep_x=ep_x, ep_y=ep_y, max_ind=max_ind, min_ind=min_ind)
        print(ccw_cw_counter+2)
        # cv2.circle(self.img, (contour[short_ind][0][0], contour[short_ind][0][1]), radius=6, color=(0, 0, 255), thickness=-1)
        # cv2.circle(self.img, (contour[max_ind][0][0], contour[max_ind][0][1]), radius=4, color=(0, 255, 0), thickness=-1)
        # cv2.circle(self.img, (contour[0][0][0], contour[0][0][1]), radius=4, color=(0, 255, 0), thickness=-1)

    def shape_detection(self, contour, epsilon, sp_x, sp_y, ep_x, ep_y, max_ind, min_ind):
        max_dist = 0
        corner_flag = False
        tp_x = self.tp_x
        tp_y = self.tp_y
        a = ep_y - sp_y
        b = sp_x - ep_x
        c = sp_y * ep_x - sp_x * ep_y
        for con in range(min_ind,max_ind):
            tp_x, tp_y = contour[con][0][0], contour[con][0][1]
            temp_dist = self.dist_betw_line_poi(a, b, c, tp_x, tp_y)

            if temp_dist >= max_dist and temp_dist >= epsilon:

                max_dist = self.dist_betw_line_poi(a, b, c, tp_x, tp_y)
                # cv2.circle(self.img, (tp_x, tp_y), radius=6, color=(0, 0, 255), thickness=-1)
                # cv2.imshow("img", self.img)
                # cv2.waitKey(0)
                min_ind = con
                corner_flag = True

        sp_x, sp_y = contour[min_ind][0][0], contour[min_ind][0][1]
        if corner_flag is True:
            self.corner_counter += 1
            # cv2.circle(self.img, (tp_x, tp_y), 7, color=(0,0,255), thickness=-1)
            # cv2.imshow("img", self.img)
            # cv2.waitKey(0)
            return self.shape_detection(contour, epsilon, sp_x=sp_x, sp_y=sp_y, ep_x=ep_x, ep_y=ep_y, max_ind=max_ind,
                                        min_ind=min_ind)

        else:
            return self.corner_counter


shape_detection = ShapeDetection()
shape_detection()


