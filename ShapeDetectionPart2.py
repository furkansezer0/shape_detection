import math


class ShapeDetection:

    def __init__(self):
        self.corner_counter = 0     # Counter of corners on contour

    # Function that calculates the distance between two points
    def dist_betw_two_poi(self, x1: int, x2: int, y1: int, y2: int):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # Function that calculates the distance between line and point
    def dist_betw_line_poi(self, a: int, b: int, c: int, x1: int, y1: int):
        distance = (abs(a * x1 + b * y1 + c)) / math.sqrt(a ** 2 + b ** 2)
        return distance

    # Main Function
    def main(self, contour, epsilon):

        sp_x, sp_y = contour[0][0][0], contour[0][0][1]     # First pixel of the contour
        max_dis = 0
        max_i = 0
        min_i = 0
        for c in range(0, len(contour)):    # Determine the furthest pixel from the first pixel of contour
            tp_x, tp_y = contour[c][0][0], contour[c][0][1]
            if self.dist_betw_two_poi(sp_x, tp_x, sp_y, tp_y) >= max_dis:
                max_dis = self.dist_betw_two_poi(sp_x, tp_x, sp_y, tp_y)
                max_i = c

        ep_x, ep_y = contour[max_i][0][0], contour[max_i][0][1]     # The furthest pixel is end point now
        self.corner_finder(contour, epsilon, sp_x, sp_y, ep_x, ep_y, max_i, min_i)      # Find the corners on the left of the line between the start and end points
        min_i = max_i
        max_i = len(contour) - 1
        sp_x, sp_y = contour[min_i][0][0], contour[min_i][0][1]
        ep_x, ep_y = contour[max_i][0][0], contour[max_i][0][1]
        self.corner_finder(contour, epsilon, sp_x, sp_y, ep_x, ep_y, max_i, min_i)      # Find the corners on the right of the line between the start and end points

        return self.corner_counter+2    # corner_counter value + 2(start and end point)

    # Find the corners on the contour
    def corner_finder(self, contour, epsilon, sp_x, sp_y, ep_x, ep_y, max_i, min_i):
        max_dist = 0
        corner_flag = False     # variable is True if the corner is found
        a = ep_y - sp_y     # a coefficient of line equation(ax+by+c)
        b = sp_x - ep_x     # b coefficient of line equation
        c = sp_y * ep_x - sp_x * ep_y       # c coefficient of line equation
        for con in range(min_i, max_i):     # Determine the furthest pixel from the line
            tp_x, tp_y = contour[con][0][0], contour[con][0][1]
            temp_dist = int(self.dist_betw_line_poi(a, b, c, tp_x, tp_y))
            if temp_dist > max_dist and temp_dist >= epsilon:   # Checks that the furthest pixel is greater than epsilon
                max_dist = int(self.dist_betw_line_poi(a, b, c, tp_x, tp_y))
                min_i = con
                corner_flag = True

        sp_x, sp_y = contour[min_i][0][0], contour[min_i][0][1]
        if corner_flag is True:     # Recursion for finding other corners
            self.corner_counter += 1
            return self.corner_finder(contour, epsilon, sp_x, sp_y, ep_x, ep_y, max_i, min_i)
