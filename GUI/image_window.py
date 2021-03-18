from PIL.ImageQt import ImageQt
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from TP0.image import MyImage


class ImageWindow(QWidget):
    def __init__(self, image: MyImage, window_title: str = None):
        super().__init__()
        self.image = image
        self.imageLabel = QLabel(alignment=(Qt.AlignVCenter | Qt.AlignHCenter))
        self.set_layouts(window_title)

    def set_layouts(self, window_title: str = None):
        # width, height = self.image.dimensions
        # self.setGeometry(30, 30, width, height)
        self.setWindowTitle(self.image.file_name if window_title is None else window_title)

        layout = QVBoxLayout()

        qim = ImageQt(self.image.pixels)
        pixmap = QPixmap.fromImage(qim).scaled(self.image.dimensions[0], self.image.dimensions[1],
                                               QtCore.Qt.KeepAspectRatio)
        # self.fileWidthLabel.setText(str(self.image.dimensions[0]))
        # self.fileHeightLabel.setText(str(self.image.dimensions[1]))
        # self.fileNameLabel.setText(self.image.file_name)
        # self.filePathLabel.setText(img.file_path)
        # self.fileLayersLabel.setText(str(len(img.channels)))

        self.setLayout(layout)
