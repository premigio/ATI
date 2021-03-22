import time

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
        gamma = window.ask_for_float('Choose a Gamma Value different from one',
                                     default=0.9, min_value=0.0, max_value=2.0, text='Gamma')
    new_image = power(image, gamma)
    new_image.show()
    return new_image


def show_hist(working_image: MyImage, window: MainWindow):
    hist = ft.histogram(working_image)

    sc = GraphWindow(window, width=5, height=4, dpi=100)
    sc.axes.bar(range(256), hist, width=1.0, align="edge")

    toolbar = NavigationToolbar(sc, window)

    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(toolbar)
    layout.addWidget(sc)

    widget = QtWidgets.QWidget()
    widget.setLayout(layout)
    return widget


def show_eq_hist(image: MyImage, window: MainWindow):
    if image is None or window is None:
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage('You must select an image first')
        error_dialog.show()
        return
    start = time.time()
    new_image = equalized_histogram2(image, draw_image=True)
    end = time.time()
    print(end - start)
    widget = show_hist(new_image, window)
    return new_image, widget
