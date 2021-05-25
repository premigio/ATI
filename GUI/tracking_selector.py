import time

from PIL.ImageQt import ImageQt
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDesktopWidget, QPushButton, QLineEdit, QHBoxLayout, \
    QFileDialog

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
        self.next_image_index = 0
        self.my_images = None
        self.iteration_images = []
        self.set_layouts()

    def set_layouts(self):
        self.center()

        self.select_images = QPushButton("Select images")
        self.select_images.clicked.connect(self.select_images_clicked)
        self.main_layout.addWidget(self.select_images)

        self.setLayout(self.main_layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_crop_finished(self):
        crop_from, crop_to = self.image_cropper.get_crop()
        epsilon = float(self.epsilonLineEdit.text())
        iterations = int(self.iterationsLineEdit.text())
        startTime = time.time()
        self.segmentation = Segmentation(self.my_image, ((crop_from.x(), crop_from.y()), (crop_to.x(), crop_to.y())),
                                         epsilon, iterations)
        finishTime = round(time.time() - startTime, 2)
        self.iteration_images = self.segmentation.get_iterations()

        # Update layout
        self.main_layout.removeWidget(self.image_cropper)
        self.epsilonLineEdit.setParent(None)
        self.epsilon_label.setParent(None)
        self.iterationsLineEdit.setParent(None)
        self.iterations_label.setParent(None)

        self.image_label = QLabel(alignment=(Qt.AlignVCenter | Qt.AlignHCenter))
        qim = ImageQt(self.iteration_images[self.iteration].image)
        pixmap = QPixmap.fromImage(qim).scaled(self.image_label.width(), self.image_label.height(),
                                               QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.main_layout.addWidget(self.image_label)

        self.time_label = QLabel("Time spent (s): " + str(finishTime), alignment=Qt.AlignRight)
        self.main_layout.addWidget(self.time_label)

        self.next_iteration_btn = QPushButton("Next iteration")
        self.next_iteration_btn.clicked.connect(self.next_iteration_clicked)
        self.main_layout.addWidget(self.next_iteration_btn)

        self.next_10_iteration_btn = QPushButton("Next 10 iterations")
        self.next_10_iteration_btn.clicked.connect(self.next_10_iterations_clicked)
        self.main_layout.addWidget(self.next_10_iteration_btn)

        self.next_image = QPushButton("Next image")
        self.next_image.clicked.connect(self.next_image_clicked)
        self.main_layout.addWidget(self.next_image)

    def next_iteration(self, step=1):
        self.iteration = self.iteration + step
        if self.iteration >= len(self.iteration_images):
            return
        qim = ImageQt(self.iteration_images[self.iteration].image)
        pixmap = QPixmap.fromImage(qim).scaled(self.image_label.width(), self.image_label.height(),
                                               QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)

    def next_iteration_clicked(self):
        self.next_iteration()

    def next_10_iterations_clicked(self):
        self.next_iteration(step=10)

    def next_image_clicked(self):

        self.next_image_index = self.next_image_index + 1

        if self.next_image_index >= len(self.my_images):
            return

        self.iteration = 0
        self.my_image = self.my_images[self.next_image_index]
        startTime = time.time()
        self.segmentation.change_image(self.my_image)
        finishTime = round(time.time() - startTime, 2)
        self.time_label.setText("Time spent (s): " + str(finishTime))
        self.iteration_images = self.segmentation.get_iterations()
        qim = ImageQt(self.iteration_images[self.iteration].image)
        pixmap = QPixmap.fromImage(qim).scaled(self.image_label.width(), self.image_label.height(),
                                               QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)

    def select_images_clicked(self):
        options = QFileDialog.Options()
        filePaths, _ = QFileDialog.getOpenFileNames(self, "Select image file", "../Photos",
                                                    "Images (*.jpg *.jpeg *.raw *.pbm *.ppm *.pgm *.RAW *.png)",
                                                    options=options)

        filePaths.sort()
        images_paths = filePaths
        self.my_images = []
        for path in images_paths:
            self.my_images.append(MyImage(path))
        self.my_image = self.my_images[0]
        width, height = self.my_image.dimensions
        self.setGeometry(30, 30, width, height)
        self.image_cropper = ImageCropper(self.my_image)
        self.image_cropper.crop_finished(self.on_crop_finished)
        self.main_layout.addWidget(self.image_cropper)

        epsilon_layout = QHBoxLayout()
        self.epsilon_label = QLabel("Epsilon: ")
        self.epsilonLineEdit = QLineEdit()
        self.epsilonLineEdit.setValidator(QDoubleValidator())
        epsilon_layout.addWidget(self.epsilon_label)
        epsilon_layout.addWidget(self.epsilonLineEdit)
        self.main_layout.addLayout(epsilon_layout)

        iterations_layout = QHBoxLayout()
        self.iterations_label = QLabel("Max iterations: ")
        self.iterationsLineEdit = QLineEdit()
        self.iterationsLineEdit.setValidator(QIntValidator())
        iterations_layout.addWidget(self.iterations_label)
        iterations_layout.addWidget(self.iterationsLineEdit)
        self.main_layout.addLayout(iterations_layout)
