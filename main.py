import cv2
from ShapeDetectionPart2 import ShapeDetection
from ArcLength import arc_length_finder

img = cv2.imread('shapes_full.png')

width = img.shape[1]
height = img.shape[0]

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    # converting image into grayscale image

_, threshold = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY)     # setting threshold of gray image
contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


for contour in contours:

    shape_detection = ShapeDetection()
    corner = shape_detection.main(contour, 0.01 * arc_length_finder(contour))

    if corner == 3:
        cv2.drawContours(img, [contour], 0, (255, 0, 0), -1)

    elif corner == 4:
        cv2.drawContours(img, [contour], 0, (0, 255, 255), -1)

    elif corner == 5:
        cv2.drawContours(img, [contour], 0, (255, 0, 255), -1)

    elif corner == 6:
        cv2.drawContours(img, [contour], 0, (0, 255, 0), -1)

    else:
        cv2.drawContours(img, [contour], 0, (0, 0, 255), -1)


cv2.imshow('shapes', img)   # displaying the image after drawing contours
cv2.waitKey(0)
cv2.destroyAllWindows()