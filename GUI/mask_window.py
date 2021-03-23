from typing import Union

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDesktopWidget, QPushButton, QInputDialog, QHBoxLayout, QLabel, \
    QLineEdit

from Algorithms import Filters
from GUI.crop_image_window import ImageCropper, CropImage
from TP0.image import MyImage


class MaskImage(QWidget):

    maskLineEdit : Union[QLineEdit, QLineEdit]

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

        # self.image_cropper = ImageCropper(self.my_image)
        # self.image_cropper.crop_finished(self.on_crop_finished)
        # main_layout.addWidget(self.image_cropper)

        mask_layout = QHBoxLayout()
        mask_label = QLabel("Mask value: ")
        self.maskLineEdit = QLineEdit()
        self.maskLineEdit.setValidator(QIntValidator(1, 20))
        mask_layout.addWidget(mask_label)
        mask_layout.addWidget(self.maskLineEdit)
        main_layout.addLayout(mask_layout)

        # Filter buttons
        median_filter_btn = QPushButton("Apply median filter")
        median_filter_btn.clicked.connect(self.median_filter)
        main_layout.addWidget(median_filter_btn)

        weigh_median_filter_btn = QPushButton("Apply wighted median filter")
        weigh_median_filter_btn.clicked.connect(self.weighted_median_filter)
        main_layout.addWidget(weigh_median_filter_btn)

        median_filter_btn = QPushButton("Apply mean filter")
        median_filter_btn.clicked.connect(self.mean_filter)
        main_layout.addWidget(median_filter_btn)

        median_filter_btn = QPushButton("Apply Gauss filter")
        median_filter_btn.clicked.connect(self.gauss_filter)
        main_layout.addWidget(median_filter_btn)

        median_filter_btn = QPushButton("Edge enhancement")
        median_filter_btn.clicked.connect(self.edge_enhancement)
        main_layout.addWidget(median_filter_btn)

        self.setLayout(main_layout)

    # FILTERs

    def median_filter(self):
        mask = int(self.maskLineEdit.text())
        if mask % 2 != 0:
            return
        new_img = Filters.median_filter(self.my_image, mask)
        new_img.image.show()

    def weighted_median_filter(self):
        new_img = Filters.weighted_median_filter(self.my_image)
        new_img.image.show()

    def mean_filter(self):
        mask = int(self.maskLineEdit.text())
        if mask % 2 != 0:
            return
        new_img = Filters.mean_filter(self.my_image, mask)
        new_img.image.show()

    def gauss_filter(self):
        # to do: sigma
        new_img = Filters.gaussian_filter(self.my_image)
        new_img.image.show()

    def edge_enhancement(self):
        # to do
        new_img = Filters.mean_filter(self.my_image, int(self.maskLineEdit.text()))
        new_img.image.show()

    # UTILs

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_crop_finished(self):
        crop_start, crop_end = self.image_cropper.get_crop()
        smaller_x, smaller_y = 0, 0

        if crop_start.x() >= crop_end.x():
            smaller_x = crop_end.x()
        else:
            smaller_x = crop_start.x()

        if crop_start.y() >= crop_end.y():
            smaller_y = crop_end.y()
        else:
            smaller_y = crop_start.y()

        self.kernel_size = smaller_x if smaller_x < smaller_y else smaller_y
        print(self.kernel_size)
