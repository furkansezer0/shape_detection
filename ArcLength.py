import math


# Function that calculates the distance between two points
def dist_betw_two_poi(x1: int, x2: int, y1: int, y2: int):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# Adds the distance between the 2 points to the total distance. When the loop ends, the length of the arc is determined
def arc_length_finder(contour):
    arc_length = 0
    for c in range(len(contour)):
        if c != len(contour) - 1:
            current_c = contour[c]
            next_c = contour[c + 1]
            arc_length += dist_betw_two_poi(current_c[0][0], next_c[0][0], current_c[0][1], next_c[0][1])
    arc_length += 1
    return arc_length
