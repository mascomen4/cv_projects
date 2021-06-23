import cv2 as cv
import numpy as np


def show_image(*args, smooth=True):
    for arg in args:
        img = cv.imread(arg)
        img_name = "img"
        if smooth:
            output = np.zeros(shape=img.shape, dtype=np.uint8)
            cv.GaussianBlur(img, (5, 5), 0, output)
            img_name = "output"
        cv.namedWindow("Example1", cv.WINDOW_AUTOSIZE)
        cv.imshow("Example1", eval(img_name))
        cv.waitKey(0)
        cv.destroyWindow("Example1")


def show_avi(path):
    cv.namedWindow("Example2", cv.WINDOW_AUTOSIZE)
    capture = cv.VideoCapture(path)
    while True:
        res, frame = capture.read()
        if not res:
            print("Can't receive frame. End?")
            break
        cv.imshow("Example2", frame)
        # wait 33 ms
        c = cv.waitKey(33)
        # if user hits Esc key (ASCII 27), then break
        if c == 27:
            break
    cv.destroyWindow("Example2")


def show_avi_trackbar(path):
    # The cvCapture object is the abstract class of the video that contains some attributes and methods
    g_capture = cv.VideoCapture(path)
    frames = int(g_capture.get(cv.CAP_PROP_FRAME_COUNT))
    g_position = 0
    cv.namedWindow("Example3", cv.WINDOW_AUTOSIZE)

    def on_trackbar_slide(pos):
        g_capture.set(cv.CAP_PROP_POS_FRAMES, pos)

    if frames != 0:
        cv.createTrackbar("Position", "Example3", g_position, frames, on_trackbar_slide)

    trackbar_pos = cv.getTrackbarPos("Position", "Example3")
    while True:
        res, frame = g_capture.read()
        if not res:
            print("Looks like you've reached the end")
            break
        cv.imshow("Example3", frame)
        trackbar_pos += 1
        cv.setTrackbarPos("Position", "Example3", trackbar_pos)
        c = cv.waitKey(33)
        if c == 27:
            break
    cv.destroyWindow("Example3")


if __name__ == '__main__':
    # show_avi_trackbar("360.avi")
    show_image("car3.jpeg")
    cv.
