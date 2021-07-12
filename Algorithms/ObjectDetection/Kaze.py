import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

from Algorithms.Classes.MyImage import MyImage


def akaze(image1: MyImage, image2: MyImage, octaves=None, threshold=50, show_detected_keypoints=True):
    akaze_cv2 = cv2.AKAZE_create(nOctaveLayers=octaves)
    return method(image1, image2, akaze_cv2, threshold, show_detected_keypoints)


def kaze(image1: MyImage, image2: MyImage, octaves=None, threshold=50, show_detected_keypoints=True):
    kaze_cv2 = cv2.KAZE_create(nOctaveLayers=octaves)
    return method(image1, image2, kaze_cv2, threshold, show_detected_keypoints)


def method(image1: MyImage, image2: MyImage, method, threshold, show_detected_keypoints):
    if image1 is None or image1.image is None or image2 is None or image2.image is None:
        return

    img1 = np.array(image1.image)
    img2 = np.array(image2.image)

    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Encuentro y dibujo los keypoints de la imagen y computo
    keypoints_1, descriptors_1 = method.detectAndCompute(img1, None)
    keypoints_2, descriptors_2 = method.detectAndCompute(img2, None)

    if show_detected_keypoints:
        img1_draw = cv2.drawKeypoints(img1, keypoints_1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        img2_draw = cv2.drawKeypoints(img2, keypoints_2, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        plt.imshow(img1_draw, cmap='gray')
        plt.show()

        plt.imshow(img2_draw, cmap='gray')
        plt.show()

    # Matcheo de features con brute force
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

    matches = bf.match(descriptors_1, descriptors_2)
    matches = sorted(matches, key=lambda x: x.distance)

    good_matches = []
    for match in matches:
        good_matches.append(match)

    final_img = cv2.drawMatches(img1, keypoints_1, img2, keypoints_2, good_matches, img2, flags=2)

    equal = len(good_matches) > threshold

    plt.imshow(final_img)
    plt.title("Images are the same: " + str(equal))
    plt.show()

    return MyImage.from_image(Image.fromarray(final_img)), equal
