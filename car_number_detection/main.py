import cv2
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from dt_template_match import dt_template_match
import imutils

image = cv.imread("data/car1.jpg")
image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
image2 = image.copy()
template = cv.imread("data/rec1.png", 0)
w, h = template.shape[::-1]

# TODO: learn What is the difference between binary, int32, float32 image? Where do they typically used?
# NOTE: All of the images should be of the same size, so that the program can find the right number from
# template size

# Perform some median filtering on the image just for the sake of my eyes
# Probably, it will also help to contour detector. And then sharpen the image to enhance the edges
median = cv.medianBlur(image2, 1)
sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
sharpen = cv.filter2D(median, -1, sharpen_kernel)

median_t = cv.medianBlur(template, 1)
sharpen_t = cv.filter2D(median_t, -1, sharpen_kernel)

# 1. Perform the Canny filtering on the image
# It performs for me the noise reduction, finds the gradients and connects the lines together.
edges = cv.Canny(median, 100, 255)
temp = cv.Canny(median_t, 50, 200)

# 2. Then we need to perform the distance transform to the edges


def find_plate_distance_transform(edges, image, image2):
    # Distance transform is quite good, I even wrote a function for that, but templates are fixed.
    # Not a good decision for my data
    dist = cv.distanceTransform(edges, cv.DIST_L2, 3)
    coord, w, h = dt_template_match(dist, temp)
    cv.rectangle(image, (coord[1], coord[0]), (coord[1]+w, coord[0]+h), 255, 2)
    cv.imshow("a", image)
    cv.rectangle(image2, coord, [coord[0]+w, coord[1]+h], 0, 3)
    cv.imshow("b", image)
    cv.waitKey()


def find_plate_contours(edges, image):
    contours = cv.findContours(edges.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None
    for contour in contours:
        perimeter = cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, 0.018*perimeter, True)
        if len(approx) == 4:
            cv.drawContours(image, [approx], 0, color=(0, 0, 0), thickness=2)
            cv.imshow("main", image)
            cv.waitKey()


if __name__ == "__main__":
    find_plate_contours(edges, image)

=======
import pandas as pd
#import tensorflow

TEMPLATE = cv.imread("data/rec.jpg", 0)
W, H = TEMPLATE.shape[::-1]

# Take example image
EXAMPLE_IMG = cv.imread("data/car1.jpg", 0)


def read_images():
    res = []
    for i in range(433):
        image = cv.imread("data/images/Cars{}.png".format(i))
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        res.append(image)
    return res


def show_rand_image(imgs):
    rand = np.random.randint(1, 200)
    cv.imshow("Sample image", imgs[rand])
    cv.waitKey()


def process_image(image):
    # Reduce the noise a little bit
    #blur = cv.medianBlur(image, 3)

    # Sharpening kernel
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpen = cv.filter2D(image, -1, kernel)

    # Automatic color correction
    #min_val, max_val, min_loc, max_loc = cv.minMaxLoc(sharpen)
    #sharpen = (sharpen - min_val)*255/(max_val - min_val)

    return sharpen


def find_plate_template(image, template):
    edges = cv.Canny(image.copy(), 100, 120)
    temp_edges = cv.Canny(template, 20, 120)

    res = cv.matchTemplate(edges, temp_edges, cv.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + W, top_left[1] + H)
    cv.rectangle(image, top_left, bottom_right, 255, 2)
    # findContours has a weird attr contours. Try to use it for recognition.
    # contours, hir = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    return image


if __name__ == "__main__":
    #images = read_images()
    #show_rand_image(images)

    processed_image = process_image(EXAMPLE_IMG)
    image = find_plate_template(processed_image, TEMPLATE)

    cv.imshow("ex", image)
    cv.waitKey()
