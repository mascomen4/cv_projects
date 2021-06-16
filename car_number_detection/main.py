import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

image = cv.imread("data/car1.jpg", 0)
image2 = image.copy()
template = cv.imread("data/number.jpeg", 0)
w, h = template.shape[::-1]

edges = cv.Canny(image, 60, 120)

# Function eval calls the function from string
# meth = "cv.TM_CCOEFF_NORMED"
# method = eval(meth)
# res = cv.matchTemplate(image, template, method)
# min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
# top_left = max_loc
# bottom_right = (top_left[0] + w, top_left[1] + h)
# cv.rectangle(image, top_left, bottom_right, 255, 2)

plt.subplot(121)
plt.imshow(image, cmap='gray')
plt.title("Original image")
plt.xticks([])
plt.yticks([])

plt.subplot(122)
plt.imshow(edges, cmap='gray')
plt.title("Edges")
plt.xticks([])
plt.yticks([])

plt.show()
