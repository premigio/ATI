import os
import sys
from typing import Optional, Union

from PIL.Image import Image
from PIL.ImageQt import ImageQt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog, QApplication, \
    QWidget, QInputDialog, QTabWidget, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt

# Subclass QMainWindow to customise your application's main window
from GUI import config_window
from GUI.crop_image_window import CropImage
from GUI.mask_window import MaskImage
from GUI.multiple_images import MultipleImageSelector
from Algorithms.Classes.MyImage import MyImage, Mode
import GUI.functions_tab as ft
import GUI.noises_filters_tab as nt
import GUI.threshold_tab as tt
import GUI.border_detector_tab as bdt

import matplotlib

from GUI.tracking_selector import TrackingSelector

matplotlib.use('Qt5Agg')


class MainWindow(QWidget):
    stacked_image: Optional[Image]
    my_image_hsv: object
    pixelY: int
    pixelX: int
    pixelLabel: Union[QLabel, QLabel]
    pixelYLineEdit: Union[QLineEdit, QLineEdit]
    pixelXLineEdit: Union[QLineEdit, QLineEdit]
    image_path_label: Union[QLabel, QLabel]
    imageNameLabel: Union[QLabel, QLabel]
    image_label: Union[QLabel, QLabel]
    myImage: Optional[MyImage]
    operations_layout: Union[QVBoxLayout, QHBoxLayout]
    op_first_img: MyImage
    op_second_img: MyImage

    def __init__(self):
        super(MainWindow, self).__init__()
        self.title = 'ATI Interface'
        self.left = 200
        self.top = 100
        self.width = 1000
        self.height = 750
        self.myImage = None
        self.stacked_image = None
        self.op_first_img = None
        self.op_second_img = None

        self.set_layouts()

        self.windows = []
        config_window.main_window_global = self

    def set_layouts(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        main_layout = QHBoxLayout()

        # Layout for image visualization
        image_preview_and_data_layout = QVBoxLayout()

        self.image_label = QLabel(alignment=(Qt.AlignVCenter | Qt.AlignHCenter))
        self.image_label.setFixedSize(300, 300)
        self.image_label.setStyleSheet(
            "QLabel { border-style: solid; border-width: 2px; border-color: rgba(0, 0, 0, 0.1); }")
        image_preview_and_data_layout.addWidget(self.image_label)

        # Layout for image data
        image_data_layout = QVBoxLayout()

        image_label_data_layout = QVBoxLayout()
        image_label_data_layout.setAlignment(Qt.AlignTop)

        image_label_layout = QHBoxLayout()
        image_label_layout.addWidget(QLabel("Name: ", objectName='title', alignment=Qt.AlignLeft))
        self.imageNameLabel = QLabel("None", alignment=Qt.AlignRight)
        image_label_layout.addWidget(self.imageNameLabel)
        image_label_data_layout.addLayout(image_label_layout)

        image_dir_layout = QHBoxLayout()
        image_dir_layout.addWidget(QLabel("Path: ", objectName='title', alignment=Qt.AlignLeft))
        self.image_path_label = QLabel("None", alignment=Qt.AlignRight)
        image_dir_layout.addWidget(self.image_path_label)
        image_label_data_layout.addLayout(image_dir_layout)

        image_height_layout = QHBoxLayout()
        image_height_layout.addWidget(QLabel("Height: ", objectName='title', alignment=Qt.AlignLeft))
        self.image_height_label = QLabel("None", alignment=Qt.AlignRight)
        image_height_layout.addWidget(self.image_height_label)
        image_label_data_layout.addLayout(image_height_layout)

        image_width_layout = QHBoxLayout()
        image_width_layout.addWidget(QLabel("Width: ", objectName='title', alignment=Qt.AlignLeft))
        self.image_width_label = QLabel("None", alignment=Qt.AlignRight)
        image_width_layout.addWidget(self.image_width_label)
        image_label_data_layout.addLayout(image_width_layout)

        number_of_pixels_layout = QHBoxLayout()
        number_of_pixels_layout.addWidget(QLabel("Number of pixels: ", objectName='title', alignment=Qt.AlignLeft))
        self.number_of_pixels_label = QLabel("None", alignment=Qt.AlignRight)
        number_of_pixels_layout.addWidget(self.number_of_pixels_label)
        image_label_data_layout.addLayout(number_of_pixels_layout)

        image_data_layout.addLayout(image_label_data_layout)

        # Layout for image actions
        self.image_actions_layout = QVBoxLayout()
        self.image_actions_layout.setAlignment(Qt.AlignTop)
        self.image_actions_layout.addWidget(QPushButton("Select image", clicked=self.select_image))

        image_data_layout.addLayout(self.image_actions_layout)
        image_preview_and_data_layout.addLayout(image_data_layout)
        main_layout.addLayout(image_preview_and_data_layout)

        # Tabs
        tabLayout = QTabWidget()
        operations_tab = QWidget()
        self.operations_layout = QVBoxLayout()
        self.operations_layout.addWidget(QPushButton("Select images", clicked=self.select_images))
        operations_tab.setLayout(self.operations_layout)

        threshold_tab = QWidget()
        threshold_layout = QVBoxLayout()
        threshold_layout.setAlignment(Qt.AlignCenter)
        threshold_layout.addWidget(QPushButton("Global threshold", clicked=self.show_global_threshold))
        threshold_layout.addWidget(QPushButton("Otsu threshold", clicked=self.show_otsu_threshold))
        threshold_tab.setLayout(threshold_layout)

        border_detector_tab = QWidget()
        border_detector_layout = QVBoxLayout()
        border_detector_layout.setAlignment(Qt.AlignCenter)
        border_detector_layout.addWidget(QPushButton("Prewitt", clicked=self.show_prewitt))
        border_detector_layout.addWidget(QPushButton("Sobel", clicked=self.show_sobel))
        border_detector_layout.addWidget(
            QPushButton("Directional border detector", clicked=self.show_directional_border))
        border_detector_layout.addWidget(QPushButton("Laplacian detector", clicked=self.show_laplacian_detector))
        border_detector_layout.addWidget(
            QPushButton("Laplacian slope detector", clicked=self.show_laplacian_slope_detector))
        border_detector_layout.addWidget(
            QPushButton("Laplacian gauss detector", clicked=self.show_laplacian_gauss_detector))
        border_detector_layout.addWidget(
            QPushButton("Canny detector", clicked=self.show_canny))
        border_detector_layout.addWidget(
            QPushButton("Susan detector", clicked=self.show_susan))
        border_detector_layout.addWidget(
            QPushButton("Hough line detector", clicked=self.show_hough_line))
        border_detector_layout.addWidget(
            QPushButton("Hough circle detector", clicked=self.show_hough_circle))
        border_detector_layout.addWidget(
            QPushButton("Segmentation", clicked=self.show_segmentation))
        border_detector_layout.addWidget(
            QPushButton("Harris corner detector", clicked=self.show_harris))
        border_detector_layout.addWidget(
            QPushButton("SIFT", clicked=self.show_sift))
        border_detector_tab.setLayout(border_detector_layout)


        filter_tab = QWidget()
        filter_layout = QVBoxLayout()
        filter_layout.setAlignment(Qt.AlignCenter)
        filter_layout.addWidget(QPushButton("Rayleigh Noise", clicked=self.show_rayleigh))
        filter_layout.addWidget(QPushButton("Gaussian Noise", clicked=self.show_gaussian_noise))
        filter_layout.addWidget(QPushButton("Exponential Noise", clicked=self.show_exponential_noise))
        filter_layout.addWidget(QPushButton("Salt n Pepper Noise", clicked=self.show_salt_n_pepper))
        filter_layout.addWidget(QPushButton("Masks and Filters", clicked=self.show_filters))
        filter_layout.addWidget(QPushButton("Bilateral Filter", clicked=self.show_bilateral_filter))
        filter_layout.addWidget(QPushButton("Anisotropic Filter", clicked=self.show_anisotropic_filter))
        filter_layout.addWidget(QPushButton("Isotropic Filter", clicked=self.show_isotropic_filter))

        filter_tab.setLayout(filter_layout)

        functions_tab = QWidget()
        functions_layout = QVBoxLayout()
        functions_layout.setAlignment(Qt.AlignCenter)
        functions_layout.addWidget(QPushButton("Generate square image", clicked=self.show_square))
        functions_layout.addWidget(QPushButton("Generate circle image", clicked=self.show_circle))
        functions_layout.addWidget(QPushButton("Power with Gamma", clicked=self.power))
        functions_layout.addWidget(QPushButton("Negative", clicked=self.show_negative))
        functions_layout.addWidget(QPushButton("Threshold", clicked=self.show_threshold))
        functions_layout.addWidget(QPushButton("Histogram", clicked=self.draw_histogram))
        functions_layout.addWidget(QPushButton("Equalized Histogram", clicked=self.draw_equalized_histogram))

        functions_tab.setLayout(functions_layout)

        tabLayout.addTab(threshold_tab, "Thresholds")
        tabLayout.addTab(border_detector_tab, "Border detectors")
        tabLayout.addTab(filter_tab, "Filters and noise")
        tabLayout.addTab(operations_tab, "Operations")
        tabLayout.addTab(functions_tab, "More functions")
        main_layout.addWidget(tabLayout)

        self.setLayout(main_layout)
        self.show()

    # ------------------------- MAIN image functions --------------------------------------------
    def get_pixel(self):
        if self.pixelXLineEdit.text() == '' or self.pixelYLineEdit.text() == '':
            return
        self.pixelX = int(self.pixelXLineEdit.text())
        self.pixelY = int(self.pixelYLineEdit.text())
        if self.myImage is not None:
            pixel = MyImage.get_pixel(self.myImage.image, (self.pixelX, self.pixelY))
            if pixel:
                self.pixelLabel.setText(str(pixel))
        else:
            # fix me: no anda, qmessage tampoco
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('You must select an image first')
            error_dialog.show()

    def set_pixel(self):
        self.pixelX = int(self.pixelXLineEdit.text())
        self.pixelY = int(self.pixelYLineEdit.text())
        if self.myImage is None:
            return
        if self.myImage.extension.lower() == 'raw':
            pixel = self.ask_for_int("Set pixel value", 0)
        else:
            r = self.ask_for_int("Enter image red", 256)
            g = self.ask_for_int("Enter image green", 256)
            b = self.ask_for_int("Enter image blue", 256)
            pixel = (r, g, b)
        self.myImage.modify_pixel((self.pixelX, self.pixelY), pixel)
        self.myImage.image.show()
        self.draw_image()

    def show_hsv(self):
        if self.myImage is not None:
            new_image = MyImage.type_conversion(self.myImage.image, Mode.HSV)
            self.my_image_hsv = new_image
            new_image.show()
            # old_path = self.myImage.path.split('.')
            # self.myImage.save_image(new_image, old_path[0] + '_hsv.' + 'png')
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('You must select an image first')
            error_dialog.show()

    def select_image(self):
        options = QFileDialog.Options()
        image_path, _ = QFileDialog.getOpenFileName(self, "Select image file", "../Photos",
                                                    "Images (*.jpg *.jpeg *.raw *.pbm *.ppm *.pgm *.RAW *.png)",
                                                    options=options)
        new_img = self.ask_for_image(image_path=image_path)

        # If its the first time uploading an image
        if self.stacked_image is None:
            self.init_main_gui()

        if new_img is not None:
            self.draw_image(new_img)
            self.stacked_image = new_img

    def init_main_gui(self):
        self.image_actions_layout.addWidget(QPushButton("Crop image", clicked=self.crop_image))
        self.image_actions_layout.addWidget(QPushButton("Convert to HSV", clicked=self.show_hsv))
        self.image_actions_layout.addWidget(QPushButton(text="Reset main image", clicked=self.reset_stack))
        pixel_actions_layout = QVBoxLayout()

        pixel_input_layout = QVBoxLayout()
        pixel_x_layout = QHBoxLayout()
        pixel_y_layout = QHBoxLayout()
        pixel_x_label = QLabel("X: ")
        self.pixelXLineEdit = QLineEdit()
        self.pixelXLineEdit.setValidator(QIntValidator())
        pixel_x_layout.addWidget(pixel_x_label)
        pixel_x_layout.addWidget(self.pixelXLineEdit)
        pixel_y_label = QLabel("Y: ")
        self.pixelYLineEdit = QLineEdit()
        self.pixelYLineEdit.setValidator(QIntValidator())
        pixel_y_layout.addWidget(pixel_y_label)
        pixel_y_layout.addWidget(self.pixelYLineEdit)
        pixel_input_layout.addLayout(pixel_x_layout)
        pixel_input_layout.addLayout(pixel_y_layout)

        show_pixel_layout = QHBoxLayout()
        show_pixel_title = QLabel("Pixel: ", alignment=Qt.AlignLeft)
        self.pixelLabel = QLabel("", alignment=Qt.AlignRight)
        show_pixel_layout.addWidget(show_pixel_title)
        show_pixel_layout.addWidget(self.pixelLabel)

        pixel_actions_layout.addLayout(pixel_input_layout)
        pixel_actions_layout.addWidget(QPushButton("Set pixel", clicked=self.set_pixel))
        pixel_actions_layout.addWidget(QPushButton("Get pixel", clicked=self.get_pixel))
        pixel_actions_layout.addLayout(show_pixel_layout)
        self.image_actions_layout.addLayout(pixel_actions_layout)

        self.image_actions_layout.update()

    def ask_for_image(self, image_path):
        if image_path is not None and image_path != '':
            file_extension = os.path.splitext(image_path)[1]
            if file_extension.lower() == ".raw":
                width = self.ask_for_int("Enter image width", 256)
                height = self.ask_for_int("Enter image height", 256)
                return MyImage(image_path, (width, height))
            else:
                return MyImage(image_path)

    def draw_image(self, img: MyImage = None):
        if img is not None:
            self.myImage = img
            self.image_width_label.setText(str(img.dimensions[0]))
            self.image_height_label.setText(str(img.dimensions[1]))
            self.number_of_pixels_label.setText(str(img.dimensions[0] * img.dimensions[1]))
            self.imageNameLabel.setText(img.file_name)
            self.image_path_label.setText(img.path)

        qim = ImageQt(self.myImage.image)
        pixmap = QPixmap.fromImage(qim).scaled(self.image_label.width(), self.image_label.height(),
                                               QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)

    def reset_stack(self):
        self.stacked_image = self.myImage
        QMessageBox.about(self, "Success", "Stacked successfully reset")

    # Generic function for extra functions tab
    def show_extra_function(self, fn):
        working_image = self.myImage if self.stacked_image is None else self.stacked_image
        return fn(working_image, self)

    def power(self):
        new_image = self.show_extra_function(ft.show_power)
        self.stacked_image = MyImage.from_image(new_image) if new_image is not None else self.stacked_image

    def show_negative(self):
        new_image = self.show_extra_function(ft.show_negative)
        self.stacked_image = MyImage.from_image(new_image) if new_image is not None else self.stacked_image

    def show_threshold(self):
        new_image = self.show_extra_function(ft.show_threshold)
        self.stacked_image = MyImage.from_image(new_image) if new_image is not None else self.stacked_image

    def draw_histogram(self):
        widget = self.show_extra_function(ft.show_hist)
        self.windows.append(widget)
        widget.show()

    def draw_equalized_histogram(self):
        new_image, widget = self.show_extra_function(ft.show_eq_hist)
        self.windows.append(widget)
        widget.show()

    # ------------------------- GENERATORS ---------------------------------------------------
    def show_square(self):
        working_image = self.myImage if self.stacked_image is None else self.stacked_image
        new_image = MyImage.create_square_image()
        new_image.show()
        self.stacked_image = new_image if new_image is not None else self.stacked_image

    def show_circle(self):
        working_image = self.myImage if self.stacked_image is None else self.stacked_image
        new_image = MyImage.create_circle_image((256, 256))
        new_image.show()
        self.stacked_image = MyImage.from_image(new_image) if new_image is not None else self.stacked_image

    # ------------------------- NOISES and FILTERS -----------------------------------------------
    # Generic function for noises
    def show_noise(self, noise):
        working_image = self.myImage if self.stacked_image is None else self.stacked_image
        new_image = noise(working_image, self)
        self.stacked_image = new_image if new_image is not None else self.stacked_image

    def show_rayleigh(self):
        self.show_noise(nt.show_rayleigh)

    def show_gaussian_noise(self):
        self.show_noise(nt.show_gaussian_noise)

    def show_exponential_noise(self):
        self.show_noise(nt.show_exponential_noise)

    def show_salt_n_pepper(self):
        self.show_noise(nt.show_salt_n_pepper_noise)

    def show_bilateral_filter(self):
        self.show_noise(nt.show_bilateral_filter)

    def show_anisotropic_filter(self):
        self.show_noise(nt.show_anisotropic_filter)

    def show_isotropic_filter(self):
        self.show_noise(nt.show_isotropic_filter)

    def show_filters(self):
        if self.myImage is not None:
            mask_image_window = MaskImage(self.stacked_image)
            self.windows.append(mask_image_window)
            mask_image_window.show()

    # ------------------------- OPERATORS ---------------------------------------------------------
    def select_images(self):
        def handler(paths):
            first_image = self.ask_for_image(paths[0])
            second_image = MyImage(paths[1], first_image.dimensions)
            self.set_operator_images(first_image, second_image)

        MultipleImageSelector(["First image", "Second image"], "Submit",
                              "Images selection", handler)

    def set_operator_images(self, first_image, second_image):
        if self.op_second_img is None and self.op_first_img is None \
                and first_image is not None and second_image is not None:
            self.init_operations_gui()

        self.op_first_img = first_image
        self.op_second_img = second_image

    def init_operations_gui(self):
        def product():
            MyImage.multiply_photos(self.op_first_img.image, self.op_second_img.image).show()

        def addition():
            MyImage.add_photos(self.op_first_img.image, self.op_second_img.image).show()

        def subtraction():
            MyImage.subtract_photos(self.op_first_img.image, self.op_second_img.image).show()

        btns_layout = QVBoxLayout()
        btns_layout.addWidget(QPushButton("Product", clicked=product))
        btns_layout.addWidget(QPushButton("Addition", clicked=addition))
        btns_layout.addWidget(QPushButton("Subtraction", clicked=subtraction))
        self.operations_layout.addLayout(btns_layout)
        self.update()

    # ------------------------- CROP ---------------------------------------------------------
    def crop_image(self):
        if self.myImage is not None:
            crop_image_window = CropImage(self.myImage)
            self.windows.append(crop_image_window)
            crop_image_window.show()

    # ------------------------- MASK ---------------------------------------------------------
    def mask_image(self):
        if self.myImage is not None:
            mask_image_window = MaskImage(self.myImage)
            self.windows.append(mask_image_window)
            mask_image_window.show()

    # ------------------------- THRESHOLDS ---------------------------------------------------------
    # Generic function for thresholds
    def show_threshold_fn(self, threshold_fn):
        working_image = self.myImage if self.stacked_image is None else self.stacked_image
        new_image = threshold_fn(working_image, self)
        self.stacked_image = new_image if new_image is not None else self.stacked_image

    def show_global_threshold(self):
        self.show_threshold_fn(tt.show_global_threshold)

    def show_otsu_threshold(self):
        self.show_threshold_fn(tt.show_otsu_threshold)

    # ------------------------- BORDER DETECTORS ---------------------------------------------------------
    # Generic function for thresholds
    def show_border_detector(self, border_detector):
        working_image = self.myImage if self.stacked_image is None else self.stacked_image
        new_image = border_detector(working_image, self)
        self.stacked_image = new_image if new_image is not None else self.stacked_image

    def show_laplacian_detector(self):
        self.show_threshold_fn(bdt.show_laplacian_detector)

    def show_laplacian_slope_detector(self):
        self.show_threshold_fn(bdt.show_laplacian_slope_detector)

    def show_laplacian_gauss_detector(self):
        self.show_threshold_fn(bdt.show_laplacian_gauss_detector)

    def show_prewitt(self):
        self.show_border_detector(bdt.show_prewitt_detector)

    def show_sobel(self):
        self.show_border_detector(bdt.show_sobel_detector)

    def show_directional_border(self):
        self.show_border_detector(bdt.show_directional_border)

    def show_canny(self):
        self.show_border_detector(bdt.show_canny_detector)

    def show_susan(self):
        self.show_border_detector(bdt.show_susan_detector)

    def show_hough_line(self):
        working_image = self.myImage if self.stacked_image is None else self.stacked_image
        w1 = bdt.show_hough_line_detector(working_image, self)
        self.windows.append(w1)
        w1.show()
        # self.windows.append(w2)
        # w2.show()

    def show_hough_circle(self):
        self.show_border_detector(bdt.show_hough_circle_detector)

    def show_segmentation(self):
        tracking_window = TrackingSelector()
        self.windows.append(tracking_window)
        tracking_window.show()

    def show_harris(self):
        self.show_border_detector(bdt.show_harris_corner_detector)

    def show_sift(self):
        self.show_border_detector(bdt.show_sift)

    # ------------------------- UTILS ---------------------------------------------------------------------
    def ask_for_int(self, message: str, default: int = 1, min_value: int = 0, max_value: int = 2147483647,
                    text: str = "Enter integer value"):
        int_val, _ = QInputDialog.getInt(self, text, message, default, min=min_value, max=max_value)
        return int_val

    def ask_for_float(self, message: str, default: float = 1, min_value: float = 0, max_value: float = 2147483647,
                      text: str = "Enter float value", decimals: int = 1):
        float_val, _ = QInputDialog.getDouble(self, text, message, default, min=min_value, max=max_value,
                                              decimals=decimals)
        return float_val


def main():
    app = QApplication(sys.argv)
    config_window.initialize()
    main_window = MainWindow()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
