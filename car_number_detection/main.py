import cv2
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from dt_template_match import dt_template_match
import imutils
import pandas as pd

# image = cv.imread("data/car1.jpg")
# image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
# image2 = image.copy()
# template = cv.imread("data/rec1.png", 0)
# w, h = template.shape[::-1]

# TODO: learn What is the difference between binary, int32, float32 image? Where do they typically used?
# NOTE: All of the images should be of the same size, so that the program can find the right number from
# template size

# Perform some median filtering on the image just for the sake of my eyes
# Probably, it will also help to contour detector. And then sharpen the image to enhance the edges

# 1. Perform the Canny filtering on the image
# It performs for me the noise reduction, finds the gradients and connects the lines together.
# 2. Then we need to perform the distance transform to the edges


def image_batch(batch_size, labeled=True):
    images = []
    path = "data/labeled/" if labeled else "data/non-labeled/"

    for i in range(batch_size):
        img = cv.imread(path + f"{i}.jpg" if labeled else f"{i+405}.jpg")
        if img is None:
            continue
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        images.append(img)
    return images


def process_images(images):
    # Probably, I need to reduce the size of the images.
    processed = []
    canny = []
    for img in images:
        median = cv.medianBlur(img, 3)
        sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpen = cv.filter2D(median, -1, sharpen_kernel)
        edges = cv.Canny(median, 100, 255)

        processed.append(sharpen)
        canny.append(edges)
    return processed, canny


def find_plate_distance_transform(edges, temp, image, image2):
    # Distance transform is quite good, I even wrote a function for that, but templates are fixed.
    # Not a good decision for my data
    dist = cv.distanceTransform(edges, cv.DIST_L2, 3)
    # Performs template matching
    coord, w, h = dt_template_match(dist, temp)
    cv.rectangle(image, (coord[1], coord[0]), (coord[1]+w, coord[0]+h), 255, 2)
    cv.imshow("a", image)
    cv.rectangle(image2, coord, [coord[0]+w, coord[1]+h], 0, 3)
    cv.imshow("b", image)
    cv.waitKey()


def find_plate_contours(edges):
    """
    :param edges: Image from Canny transform
    :return: 2D Matrix where 0 axis is images, and 1 axis is the contours in images
    """
    imgs_contours = []
    for img_edge in edges:
        contours = cv.findContours(img_edge.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        found_cnts = []
        for contour in contours:
            perimeter = cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, 0.018*perimeter, True)
            if len(approx) == 4:
                found_cnts.append(approx)
        imgs_contours.append(found_cnts)
    return imgs_contours


def draw_contours(images, contours):
    # WARNING: PLOTS THE CONTOURS DIRECTLY ON THE GIVEN IMAGES.
    for i, image in enumerate(images):
        cv.drawContours(image, contours[i], -1, color=(10,255,255), thickness=4)


def write_images(images, path):
    for i, image in enumerate(images):
        cv.imwrite(path + f"{i}.jpg", image)


def elongation(m):
    x = m['mu20'] + m['mu02']
    y = 4 * m['mu11']**2 + (m['mu20'] - m['mu02'])**2
    return (x + y**0.5) / (x - y**0.5)


def find_moments(contours):
    mu = [None] * len(contours)
    for i in range(len(contours)):
        mu[i] = cv.moments(contours[i])
    return mu


# TODO: Find the elongation for each contour, then print that for each CLOSED contour. Notice what elongation
#  has the number plate.
#  Also, try to play with trackBar of Canny thresh (the code is in test.py)


imgs = image_batch(13)
imgs2 = imgs.copy()
imgs, canny = process_images(imgs)
approxes = find_plate_contours(canny)
draw_contours(imgs2, approxes)
path = "data/plotted-data/"
write_images(imgs2, path)