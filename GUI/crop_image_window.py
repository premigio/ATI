import numpy
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDesktopWidget, QPushButton, QHBoxLayout

from GUI import crop_image_utils
from GUI.image_cropper import ImageCropper
from TP0.image import MyImage


class CropImage(QWidget):
    def __init__(self, img: MyImage = None):
        super().__init__()
        self.my_image = img
        self.set_layouts()

    def set_layouts(self):
        width, height = self.my_image.dimensions
        self.setGeometry(30, 30, width, height)
        self.setWindowTitle(self.my_image.file_name)
        self.center()

        main_layout = QVBoxLayout()

        self.image_cropper = ImageCropper(self.my_image)
        self.image_cropper.crop_finished(self.on_crop_finished)
        main_layout.addWidget(self.image_cropper)

        # Labels for number of pixels, average grey and colour levels
        number_of_pixels_layout = QHBoxLayout()
        number_of_pixels_layout.addWidget(QLabel("Number of pixels: ", objectName='title', alignment=Qt.AlignLeft))
        self.number_of_pixels_label = QLabel("None", alignment=Qt.AlignRight)
        number_of_pixels_layout.addWidget(self.number_of_pixels_label)
        main_layout.addLayout(number_of_pixels_layout)

        self.is_grey_scale = MyImage.is_grey_scale(self.my_image.image)
        if self.is_grey_scale:
            grey_avg_layout = QHBoxLayout()
            grey_avg_layout.addWidget(QLabel("Grey average level: ", objectName='title', alignment=Qt.AlignLeft))
            self.avg_label = QLabel("None", alignment=Qt.AlignRight)
            grey_avg_layout.addWidget(self.avg_label)
            main_layout.addLayout(grey_avg_layout)
        else:
            rgb_avg_layout = QHBoxLayout()
            rgb_avg_layout.addWidget(QLabel("RGB average level: ", objectName='title', alignment=Qt.AlignLeft))
            self.avg_label = QLabel("None", alignment=Qt.AlignRight)
            rgb_avg_layout.addWidget(self.avg_label)
            main_layout.addLayout(rgb_avg_layout)

        self.btn_save = QPushButton("Save")
        self.btn_save.clicked.connect(self.on_save_clicked)
        self.btn_save.setEnabled(False)
        main_layout.addWidget(self.btn_save)

        self.setLayout(main_layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_crop_finished(self):
        self.btn_save.setEnabled(True)

    def on_save_clicked(self):
        img_left = crop_image_utils.get_cropped_image(self.my_image.image, self.image_cropper.get_crop())

        # Get image data
        np_img = numpy.array(img_left)

        if self.is_grey_scale:
            avg_level = numpy.mean(numpy.mean(np_img, axis=0), axis=0)
        else:
            avg_level = numpy.mean(numpy.mean(numpy.mean(np_img, axis=0), axis=0), axis=0)

        self.avg_label.setText(str(avg_level))
        self.number_of_pixels_label.setText(str(np_img.shape[0] * np_img.shape[1]))

        # Show image
        img_left.show()
