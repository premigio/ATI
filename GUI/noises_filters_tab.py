import numpy
from PIL.ImageQt import ImageQt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDesktopWidget, QPushButton, QHBoxLayout

from GUI import config_window
from GUI.main_window import *
from TP0.image import MyImage

from Algorithms.Noises import *


def show_rayleigh(image: MyImage, window):
    if image is None or window is None:
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage('You must select an image first')
        error_dialog.show()
        return
    epsilon = window.ask_for_float('Choose an Epsilon Value',
                                   default=0.5, min_value=0.0, text='epsilon')
    percentage = window.ask_for_float('Choose a percentage Value',
                                      default=30.0, min_value=0.0, max_value=100.0, text='Percentage')
    new_image = rayleigh_multiplicative(image, percentage / 100.0, epsilon)
    new_image.image.show()
    return new_image


def show_gaussian_noise(image: MyImage, window):
    if image is None or window is None:
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage('You must select an image first')
        error_dialog.show()
        return
    mean = window.ask_for_float('Choose a mean',
                                default=20.0, min_value=0.0, text='Mean')
    deviation = window.ask_for_float('Choose a standard deviation',
                                     default=0.5, min_value=0.0, text='Deviation')
    percentage = window.ask_for_float('Choose a percentage Value',
                                      default=30.0, min_value=0.0, max_value=100.0, text='Percentage')
    new_image = gaussian_additive(image, percentage / 100.0, mean, deviation)
    new_image.image.show()
    return new_image


def show_exponential_noise(image: MyImage, window):
    if image is None or window is None:
        return
    lambda_param = window.ask_for_float('Choose a lambda value',
                                        default=20.0, min_value=0.0, text='Lambda')
    percentage = window.ask_for_float('Choose a percentage value',
                                      default=30.0, min_value=0.0, max_value=100.0, text='Percentage')
    new_image = exponential_multiplicative(image, percentage=percentage / 100.0, lambda_param=lambda_param)
    new_image.image.show()
    return new_image


def show_salt_n_pepper_noise(image: MyImage, window):
    if image is None or window is None:
        return
    density = window.ask_for_float('Choose a density value',
                                        default=50.0, min_value=0.0, max_value=100.0, text='Density')
    new_image = salt_n_pepper(image, density/100.0)
    new_image.image.show()
    return new_image
