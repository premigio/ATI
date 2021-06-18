import cv2
import numpy as np
import cv2 as cv
from PIL import Image
from matplotlib import pyplot as plt

from Algorithms.Classes.MyImage import *


def __grey_photo(img, mode):
    return cv.cvtColor(img, cv.COLOR_RGB2GRAY) if mode == 'RGB' else img


# default es None, que en realidad es d=3 por como esta en el paper
def sift_algorithm(image1: MyImage, image2, octaves=None,
                   show_detected_keypoints=True):
    if image1 is None or image1.image is None or image2 is None or image2.image is None:
        return

    img1 = np.array(image1.image)
    img2 = np.array(image2.image)

    # Quiero Greyscale, al pepe colores. Uso de esta vez to grayscale porque me pinto
    img1 = __grey_photo(img1, image1.mode)
    img2 = __grey_photo(img2, image1.mode)

    sift = cv.SIFT_create(nOctaveLayers=octaves)

    # Encuentro y dibujo los keypoints de la imagen y computo
    kp1, descriptor1 = sift.detectAndCompute(img1, None)
    kp2, descriptor2 = sift.detectAndCompute(img2, None)

    # img1_draw = cv.drawKeypoints(img1, kp1, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # img2_draw = cv.drawKeypoints(img2, kp2, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    #
    # if show_detected_keypoints:
    #     plt.imshow(img1_draw, cmap='gray')
    #     plt.show()
    #
    #     plt.imshow(img2_draw, cmap='gray')
    #     plt.show()

    # matcher = cv.BFMatcher(cv2.NORM_L1, crossCheck=True)
    # matches = matcher.match(descriptor1, descriptor2, neighbours)
    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(descriptor1, descriptor2, k=2)

    # Need to draw only good matches, so create a mask
    matchesMask = [[0, 0] for i in range(len(matches))]

    # ratio test as per Lowe's paper
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7 * n.distance:
            matchesMask[i] = [1, 0]
    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                       matchesMask=matchesMask,
                       flags=cv.DrawMatchesFlags_DEFAULT)
    final_image = cv.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)

    plt.imshow(final_image)
    plt.show()

    return MyImage.from_image(Image.fromarray(final_image))
