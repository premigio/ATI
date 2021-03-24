from typing import Union

from PIL import Image
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDesktopWidget, QPushButton, QInputDialog, QHBoxLayout, QLabel, \
    QLineEdit

from Algorithms import Filters
from GUI import crop_image_utils
from GUI.crop_image_window import ImageCropper, CropImage
from GUI.graph_window import GraphWindow
from TP0.image import MyImage


class MaskImage(QWidget):
    maskLineEdit: Union[QLineEdit, QLineEdit]
    image_cropper: ImageCropper
    selected_region: Image

    def __init__(self, img: MyImage = None):
        super().__init__()
        self.my_image = img
        self.set_layouts()
        self.selected_region = img

    def set_layouts(self):
        width, height = self.my_image.dimensions
        self.setGeometry(30, 30, width, height)
        self.setWindowTitle(self.my_image.file_name)
        self.center()

        main_layout = QVBoxLayout()

        # Image cropper to select region to apply filter
        self.image_cropper = ImageCropper(self.my_image)
        self.image_cropper.crop_finished(self.on_crop_finished)
        main_layout.addWidget(self.image_cropper)

        # Ask for mask value, min: 1, max: 20?
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

        weigh_median_filter_btn = QPushButton("Apply weighted median filter")
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
        mask = self.maskLineEdit.text()
        if mask == '':
            return
        mask = int(mask)
        if mask is None or mask % 2 == 0:
            return
        filtered_img = Filters.median_filter(self.selected_region, mask)
        result = MyImage.merge_images(self.my_image.image, filtered_img.image, self.image_cropper.get_crop()) \
            if self.image_cropper.get_crop() != (None, None) else filtered_img
        result.show()

    def weighted_median_filter(self):
        filtered_img = Filters.weighted_median_filter(self.selected_region)
        result = MyImage.merge_images(self.my_image.image, filtered_img.image, self.image_cropper.get_crop()) \
            if self.image_cropper.get_crop() != (None, None) else filtered_img
        result.show()

    def mean_filter(self):
        mask = self.maskLineEdit.text()
        if mask == '':
            return
        mask = int(mask)
        if mask is None or mask % 2 == 0:
            return
        filtered_img = Filters.mean_filter(self.selected_region, mask)
        result = MyImage.merge_images(self.my_image.image, filtered_img.image, self.image_cropper.get_crop()) \
            if self.image_cropper.get_crop() != (None, None) else filtered_img
        result.show()

    def gauss_filter(self):
        sigma, _ = QInputDialog.getInt(self, 'sigma', 'Insert sigma value: ', 1, min=1, max=10)
        filtered_img = Filters.gaussian_filter(self.selected_region, sigma)
        result = MyImage.merge_images(self.my_image.image, filtered_img.image, self.image_cropper.get_crop()) \
            if self.image_cropper.get_crop() != (None, None) else filtered_img
        result.show()

    def edge_enhancement(self):
        mask = self.maskLineEdit.text()
        if mask == '':
            return
        mask = int(mask)
        if mask is None or mask % 2 == 0:
            return
        filtered_img = Filters.border_enhancement(self.selected_region, mask)
        result = MyImage.merge_images(self.my_image.image, filtered_img.image, self.image_cropper.get_crop()) \
            if self.image_cropper.get_crop() != (None, None) else filtered_img
        result.show()

    # UTILs

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_crop_finished(self):
        cropped_img = crop_image_utils.get_cropped_image(self.my_image.image, self.image_cropper.get_crop())
        self.selected_region = MyImage.from_image(cropped_img, cropped_img.size)
