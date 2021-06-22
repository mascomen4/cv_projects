import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


def dt_template_match(dt_image, template):
    """
    let's assume we have DT (Distance Transform) and Template. W, H - are dimensions of the DT. w,h - are dims of the
    Template (only black and white pixels).
    So, I need to get the coordinates of black pixels in Template.
    :param dt_image: Distance transformed image
    :param template: Image with only 2 values: 0 and 255, where 0 - black, 255 - white
    :return: coordinate,w,h from which can be the best fit rectangle reconstructed
    """
    coords = np.column_stack(np.where(template > 240))
    dt_w, dt_h = dt_image.shape[::-1]
    w, h = template.shape[::-1]
    max_sum = -1
    max_coord = 0
    for row in range(dt_h-h):
        for column in range(dt_w-w):
            sum_ = 0
            for coord in coords:
                sum_ += dt_image[row + coord[0]][column + coord[1]]
            if sum_ > max_sum:
                max_sum = sum_
                max_coord = [row, column]
    return max_coord, w, h
