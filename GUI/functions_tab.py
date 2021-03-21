import numpy
from PIL.ImageQt import ImageQt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDesktopWidget, QPushButton, QHBoxLayout

from GUI import config_window
from GUI.main_window import *
from TP0.image import MyImage
from Algorithms.Functions import *


def show_power(image: MyImage, window: MainWindow):
    if image is None or window is None:
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage('You must select an image first')
        error_dialog.show()
        return
    gamma = 1.0
    while gamma == 1.0:
        gamma = window.ask_for_float('Choose a Gamma Value different form one',
                                     default=0.9, min_value=0.0, max_value=2.0, text='Gamma')
    new_image = power(image, gamma)
    new_image.show()
    return new_image
