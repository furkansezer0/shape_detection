import cv2

# reading image
img = cv2.imread('shapes_full.png')

# converting image into grayscale image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# setting threshold of gray image
_, threshold = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY)


# using a findContours() function
contours, _ = cv2.findContours(
    threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)



for contour in contours:

    # cv2.approxPloyDP() function to approximate the shape
    approx = cv2.approxPolyDP(
        contour, 0.0175 * cv2.arcLength(contour, True), True)


    if len(approx) == 3:
        cv2.drawContours(img, [contour], 0, (0, 255, 0), -1)

    elif len(approx) == 4:
        cv2.drawContours(img, [contour], 0, (0, 255, 255), -1)

    elif len(approx) == 5:
        cv2.drawContours(img, [contour], 0, (255, 0, 255), -1)

    elif len(approx) == 6:
        cv2.drawContours(img, [contour], 0, (255, 255, 0), -1)

    else:
        cv2.drawContours(img, [contour], 0, (255, 0, 0), -1)

# displaying the image after drawing contours
cv2.imshow('shapes', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
