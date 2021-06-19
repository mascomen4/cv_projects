import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
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