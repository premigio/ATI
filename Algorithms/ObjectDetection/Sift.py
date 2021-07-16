import cv2
import numpy as np
import cv2 as cv
from PIL import Image
from matplotlib import pyplot as plt

from Algorithms.Classes.MyImage import *


def __grey_photo(img, mode):
    return cv.cvtColor(img, cv.COLOR_RGB2GRAY) if mode == 'RGB' else img


def sift_algorithm(image1: MyImage, image2, octaves=None, threshold=100,
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

    if show_detected_keypoints:
        img1_draw = cv.drawKeypoints(img1, kp1, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        img2_draw = cv.drawKeypoints(img2, kp2, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        plt.imshow(img1_draw, cmap='gray')
        plt.show()

        plt.imshow(img2_draw, cmap='gray')
        plt.show()

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

    count = filter(lambda a: a == [1, 0], matchesMask)
    count = len(list(count))
    print(count)
    equal = count > threshold

    plt.imshow(final_image)
    plt.title("Boolean to show whether images are the same: " + str(equal))
    plt.show()

    return MyImage.from_image(Image.fromarray(final_image)), equal


# default es None, que en realidad es d=3 por como esta en el paper
def affine_skew(t, phi, img):
    h, w = img.shape[:2]

    mask = np.zeros((h, w), np.uint8)
    mask[:] = 255

    A = np.float32([[1, 0, 0], [0, 1, 0]])

    # Rotate image
    if phi != 0.0:
        phi = np.deg2rad(phi)
        s, c = np.sin(phi), np.cos(phi)
        A = np.float32([[c, -s], [s, c]])
        corners = [[0, 0], [w, 0], [w, h], [0, h]]
        tcorners = np.int32(np.dot(corners, A.T))
        x, y, w, h = cv.boundingRect(tcorners.reshape(1, -1, 2))
        A = np.hstack([A, [[-x], [-y]]])
        img = cv.warpAffine(img, A, (w, h), flags=cv.INTER_LINEAR, borderMode=cv.BORDER_REPLICATE)

    # Tilt image (resizing after rotation)
    if t != 1.0:
        s = 0.8 * np.sqrt(t * t - 1)
        img = cv.GaussianBlur(img, (0, 0), sigmaX=s, sigmaY=0.01)
        img = cv.resize(img, (0, 0), fx=1.0 / t, fy=1.0, interpolation=cv.INTER_NEAREST)
        A[0] /= t

    if phi != 0.0 or t != 1.0:
        h, w = img.shape[:2]
        mask = cv.warpAffine(mask, A, (w, h), flags=cv.INTER_NEAREST)

    Ai = cv.invertAffineTransform(A)

    return img, mask, Ai


def affine_detect(sift, img):
    key_points = []
    descriptors = []

    # Preparo primero todas las transformaciones afin buscando los valores distintos del tilt y de phi
    params = [(1.0, 0.0)]
    for t in 2 ** (0.5 * np.arange(1, 6)):
        for phi in np.arange(0, 180, 72.0 / t):
            params.append((t, phi))

    for t, phi in params:
        a_img, mask, Ai = affine_skew(t, phi, img)
        kp, dc = sift.detectAndCompute(a_img, mask)

        for k in kp:
            x, y = k.pt
            k.pt = tuple(np.dot(Ai, (x, y, 1)))

        key_points = [*key_points, *kp]
        descriptors = [*descriptors, *dc]

    return key_points, np.array(descriptors)


def asift_algorithm(image1: MyImage, image2, octaves=None, threshold=100, only_lines=False):
    if image1 is None or image1.image is None or image2 is None or image2.image is None:
        return

    img1 = np.array(image1.image)
    img2 = np.array(image2.image)

    # Quiero Greyscale, al pepe colores. Uso de esta vez to grayscale porque me pinto
    img1 = __grey_photo(img1, image1.mode)
    img2 = __grey_photo(img2, image1.mode)

    sift = cv.SIFT_create(nOctaveLayers=octaves)

    kp1, descriptor1 = affine_detect(sift, img1)
    kp2, descriptor2 = affine_detect(sift, img2)

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

    flag = cv.DrawMatchesFlags_DEFAULT if not only_lines else cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                       matchesMask=matchesMask,
                       flags=flag)
    final_image = cv.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)

    count = filter(lambda a: a == [1, 0], matchesMask)
    count = len(list(count))
    print("Number of values that passed as equivalent: " + str(count))
    equal = count > threshold

    plt.imshow(final_image)
    plt.title("Boolean to show whether images are the same: " + str(equal))
    plt.show()

    return MyImage.from_image(Image.fromarray(final_image)), equal
