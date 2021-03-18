import os
import sys
from typing import Optional, Union

from PIL.ImageQt import ImageQt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog, QApplication, \
    QWidget, QInputDialog, QTabWidget, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt

# Subclass QMainWindow to customise your application's main window
from GUI.image_window import ImageWindow
from GUI.operations_window import OperationsBetweenImages
from TP0.image import MyImage, Mode
from TP0.main import sizeDict


class MainWindow(QWidget):
    pixelY: int
    pixelX: int
    tabLayout: Union[QTabWidget, QTabWidget]
    pixelLabel: Union[QLabel, QLabel]
    pixelYLineEdit: Union[QLineEdit, QLineEdit]
    pixelXLineEdit: Union[QLineEdit, QLineEdit]
    image_path_label: Union[QLabel, QLabel]
    imageNameLabel: Union[QLabel, QLabel]
    image_label: Union[QLabel, QLabel]
    myImage: Optional[MyImage]

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.title = 'ATI Interface'
        self.left = 200
        self.top = 100
        self.width = 1000
        self.height = 750
        self.myImage = None

        self.set_layouts()

        self.views = []

    def set_layouts(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        main_layout = QHBoxLayout()

        # IMAGE 1

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

        # imageHeightLayout = QHBoxLayout()
        # imageHeightLayout.addWidget(QLabel("Height: ", objectName='title', alignment=Qt.AlignLeft))
        # self.imageHeightLabel = QLabel("None", alignment=Qt.AlignRight)
        # imageHeightLayout.addWidget(self.imageHeightLabel)
        # image_label_data_layout.addLayout(imageHeightLayout)
        #
        # imageWidthLayout = QHBoxLayout()
        # imageWidthLayout.addWidget(QLabel("Width: ", objectName='title', alignment=Qt.AlignLeft))
        # self.imageWidthLabel = QLabel("None", alignment=Qt.AlignRight)
        # imageWidthLayout.addWidget(self.imageWidthLabel)
        # image_label_data_layout.addLayout(imageWidthLayout)

        image_data_layout.addLayout(image_label_data_layout)

        # Layout for image actions
        image_actions_layout = QVBoxLayout()
        image_actions_layout.setAlignment(Qt.AlignTop)
        image_actions_layout.addWidget(QPushButton("Select image", clicked=self.select_image))
        image_actions_layout.addWidget(QPushButton("Convert to HSV", clicked=self.show_hsv))

        pixel_actions_layout = QVBoxLayout()

        pixel_input_layout = QVBoxLayout()
        pixel_x_layout = QHBoxLayout()
        pixel_y_layout = QHBoxLayout()
        pixel_x_label = QLabel("X: ")
        # xIntValidator = QIntValidator(0, self.myImage.dimensions[0]) if self.myImage is not None else QIntValidator()
        self.pixelXLineEdit = QLineEdit()
        self.pixelXLineEdit.setValidator(QIntValidator())
        pixel_x_layout.addWidget(pixel_x_label)
        pixel_x_layout.addWidget(self.pixelXLineEdit)
        pixel_y_label = QLabel("Y: ")
        # yIntValidator = QIntValidator(0, self.myImage.dimensions[1]) if self.myImage is not None else QIntValidator()
        self.pixelYLineEdit = QLineEdit()
        self.pixelYLineEdit.setValidator(QIntValidator())
        pixel_y_layout.addWidget(pixel_y_label)
        pixel_y_layout.addWidget(self.pixelYLineEdit)
        pixel_input_layout.addLayout(pixel_x_layout)
        pixel_input_layout.addLayout(pixel_y_layout)

        get_pixel_layout = QVBoxLayout()
        get_pixel_layout.addWidget(QPushButton("Get pixel", clicked=self.get_pixel))
        show_pixel_layout = QHBoxLayout()
        show_pixel_title = QLabel("Pixel: ", alignment=Qt.AlignLeft)
        self.pixelLabel = QLabel("", alignment=Qt.AlignRight)
        show_pixel_layout.addWidget(show_pixel_title)
        show_pixel_layout.addWidget(self.pixelLabel)
        get_pixel_layout.addLayout(show_pixel_layout)

        pixel_actions_layout.addLayout(pixel_input_layout)
        pixel_actions_layout.addWidget(QPushButton("Set pixel", clicked=self.set_pixel))
        pixel_actions_layout.addLayout(get_pixel_layout)
        image_actions_layout.addLayout(pixel_actions_layout)

        image_data_layout.addLayout(image_actions_layout)
        image_preview_and_data_layout.addLayout(image_data_layout)
        main_layout.addLayout(image_preview_and_data_layout)

        # Tabs
        self.tabLayout = QTabWidget()
        operations_tab = QWidget()
        operations_layout = QHBoxLayout()
        operations_button = QPushButton("Operations between Images", clicked=self.operation_between_images)
        operations_layout.addWidget(operations_button)
        operations_tab.setLayout(operations_layout)

        generator_tab = QWidget()
        side_actions_layout = QVBoxLayout()
        side_actions_layout.setAlignment(Qt.AlignCenter)
        side_actions_layout.addWidget(QPushButton("Generate square image", clicked=self.show_square))
        side_actions_layout.addWidget(QPushButton("Generate circle image", clicked=self.show_circle))
        generator_tab.setLayout(side_actions_layout)

        self.tabLayout.addTab(operations_tab, "Operations")
        self.tabLayout.addTab(generator_tab, "Generator")
        main_layout.addWidget(self.tabLayout)

        self.setLayout(main_layout)
        self.show()

    @staticmethod
    def show_square():
        MyImage.create_square_image().show()

    @staticmethod
    def show_circle():
        MyImage.create_circle_image().show()

    def get_pixel(self):
        self.pixelX = int(self.pixelXLineEdit.text())
        self.pixelY = int(self.pixelYLineEdit.text())
        if self.myImage is not None:
            pixel = MyImage.get_pixel(self.myImage.image, (self.pixelX, self.pixelY))
            if pixel:
                self.pixelLabel.setText(str(pixel))
        else:
            # no anda, qmessage tampoco
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('You must select an image first')
            error_dialog.show()

    def set_pixel(self):
        if self.myImage is not None:
            pixel = self.ask_for_int("Set pixel value", 0)
            MyImage.modify_pixel(self.myImage, (self.pixelX, self.pixelY), pixel)
            self.draw_image(self.myImage)

    def show_hsv(self):
        if self.myImage is not None:
            MyImage.type_conversion(self.myImage.image, Mode.HSV)
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('You must select an image first')
            error_dialog.show()

    def operation_between_images(self):
        if self.myImage is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('More information')
            msg.setWindowTitle("Error")
            return msg
        else:
            self.views.append(OperationsBetweenImages())

    def select_image(self):
        options = QFileDialog.Options()
        image_path, _ = QFileDialog.getOpenFileName(self, "Select image file", "",
                                                    "Images (*.jpg *.jpeg *.raw *.pbm *.ppm *.pgm *.RAW *.png)",
                                                    options=options)
        return self.ask_for_image(image_path=image_path)

    def ask_for_image(self, image_path):
        if image_path is not None and image_path != '':
            file_extension = os.path.splitext(image_path)[1]
            if file_extension.lower() == ".raw":
                width = self.ask_for_int("Enter image width", 256)
                height = self.ask_for_int("Enter image height", 256)
                self.draw_image(MyImage(image_path, (width, height)))
            else:
                self.draw_image(MyImage(image_path))
                return True
        else:
            return False


    def draw_image(self, img: MyImage = None):
        if img is not None:
            self.myImage = img
            # self.imageWidthLabel.setText(str(img.dimensions[0]))
            # self.imageHeightLabel.setText(str(img.dimensions[1]))
            self.imageNameLabel.setText(img.file_name)
            self.image_path_label.setText(img.path)

        qim = ImageQt(self.myImage.image)
        pixmap = QPixmap.fromImage(qim).scaled(self.image_label.width(), self.image_label.height(),
                                               QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)

    def ask_for_int(self, message: str, default: int = 1, min: int = 1, max: int = 2147483647,
                    text: str = "Enter integer value"):
        int_val, _ = QInputDialog.getInt(self, text, message, default, min=min, max=max)
        return int_val


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
