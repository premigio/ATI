from PIL.ImageQt import ImageQt
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDesktopWidget, QPushButton

from Algorithms.Classes.MyImage import MyImage
from Algorithms.EdgeDetection.Segmentation import Segmentation
from GUI.image_cropper import ImageCropper


class TrackingSelector(QWidget):
    def __init__(self, img: MyImage = None):
        super().__init__()
        self.my_image = img
        self.segmentation: Segmentation
        self.main_layout = QVBoxLayout()
        self.iteration = 0
        self.set_layouts()

    def set_layouts(self):
        width, height = self.my_image.dimensions
        self.setGeometry(30, 30, width, height)
        self.setWindowTitle(self.my_image.file_name)
        self.center()

        self.image_cropper = ImageCropper(self.my_image)
        self.image_cropper.crop_finished(self.on_crop_finished)
        self.main_layout.addWidget(self.image_cropper)

        self.setLayout(self.main_layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_crop_finished(self):
        crop_from, crop_to = self.image_cropper.get_crop()
        self.segmentation = Segmentation(self.my_image, ((crop_from.x(), crop_from.y()), (crop_to.x(), crop_to.y())),
                                         100000, 0.9)
        # self.my_image = self.segmentation.get_image_edges()
        self.images = self.segmentation.get_iterations()

        # Update layout
        self.main_layout.removeWidget(self.image_cropper)

        self.image_label = QLabel(alignment=(Qt.AlignVCenter | Qt.AlignHCenter))
        qim = ImageQt(self.images[self.iteration].image)
        pixmap = QPixmap.fromImage(qim).scaled(self.image_label.width(), self.image_label.height(),
                                               QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.main_layout.addWidget(self.image_label)

        self.next_iteration = QPushButton("Next iteration")
        self.next_iteration.clicked.connect(self.next_iteration_clicked)
        self.main_layout.addWidget(self.next_iteration)

        self.next_image = QPushButton("Next image")
        self.next_image.clicked.connect(self.next_iteration_clicked)
        self.main_layout.addWidget(self.next_image)

    def next_iteration_clicked(self):
        # self.segmentation.change_image()
        # qim = ImageQt(self.my_image.image)
        # pixmap = QPixmap.fromImage(qim).scaled(self.image_label.width(), self.image_label.height(),
        #                                        QtCore.Qt.KeepAspectRatio)
        # self.image_label.setPixmap(pixmap)
        self.iteration = self.iteration + 1
        qim = ImageQt(self.images[self.iteration].image)
        pixmap = QPixmap.fromImage(qim).scaled(self.image_label.width(), self.image_label.height(),
                                               QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)

