import numpy
from PIL.ImageQt import ImageQt
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDesktopWidget, QPushButton, QHBoxLayout

from GUI import config_window
from TP0.image import MyImage


class CropImage(QWidget):
    def __init__(self, img: MyImage = None, window_title: str = None):
        super().__init__()
        self.my_image = img
        self.set_layouts(window_title)

    def set_layouts(self, window_title: str = None):
        width, height = self.my_image.dimensions
        self.setGeometry(30, 30, width, height)
        self.setWindowTitle(self.my_image.file_name if window_title is None else window_title)
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

        is_grey_scale = MyImage.is_grey_scale(self.my_image.image)
        if is_grey_scale:
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

        # Save button
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
        cropped_image = self.image_cropper.new_img
        np_img = numpy.array(cropped_image)
        # Fix me: IndexError: tuple index out of range
        # self.avg_label = numpy.mean(np_img, axis=2)
        # Fix me: no probé esto, pero hay que poner la cantidad de pixeles de la foto croppeada
        # self.number_of_pixels_label = cropped_image.size ?
        self.btn_save.setEnabled(True)

    def on_save_clicked(self):
        img = self.my_image.image
        crop_start, crop_end = self.image_cropper.get_crop()

        bigger_x, smaller_x, bigger_y, smaller_y = 0, 0, 0, 0

        if crop_start.x() >= crop_end.x():
            bigger_x = crop_start.x()
            smaller_x = crop_end.x()
        else:
            bigger_x = crop_end.x()
            smaller_x = crop_start.x()

        if crop_start.y() >= crop_end.y():
            bigger_y = crop_start.y()
            smaller_y = crop_end.y()
        else:
            bigger_y = crop_end.y()
            smaller_y = crop_start.y()

        img_left_area = (smaller_x, smaller_y, bigger_x, bigger_y)

        img_left = img.crop(img_left_area)

        img_left.show()
        """cropped_img = img.crop(crop_start.x(), crop_start.y(),
                               crop_end.x(), crop_end.y()).show()"""


class ImageCropper(QWidget):
    def __init__(self, image: MyImage):
        super().__init__()
        self.my_image = image
        self.new_img = None
        self.image_label = QLabel(alignment=(Qt.AlignVCenter | Qt.AlignHCenter))
        self.image_label.setFixedSize(300, 300)
        self.image_label.setStyleSheet(
            "QLabel { border-style: solid; border-width: 2px; border-color: rgba(0, 0, 0, 0.1); }")
        qim = ImageQt(self.my_image.image)
        pixmap = QPixmap.fromImage(qim).scaled(self.my_image.dimensions[0], self.my_image.dimensions[1],
                                               QtCore.Qt.KeepAspectRatio)
        self.drawn_image = pixmap
        self.image_label.setPixmap(pixmap)
        self.crop_start = None
        self.crop_end = None
        self.drawing = False
        self.lastPoint = QPoint()
        self.curr_pointer = None
        self.handler_crop_finished = None

        self.set_layouts()

    def set_layouts(self):
        width, height = self.my_image.dimensions
        self.setFixedSize(width, height)
        self.setWindowTitle(self.my_image.file_name)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def crop_finished(self, handler_crop_finished):
        self.handler_crop_finished = handler_crop_finished

    def get_crop(self):
        return self.crop_start, self.crop_end

    # EVENTS
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.crop_start = event.pos()
        elif event.button() == Qt.RightButton:
            self.drawing = False
            self.crop_start = None
            self.crop_end = None
            self.update()
        elif event.button() == Qt.MiddleButton:

            crop_start, crop_end = self.get_crop()

            if crop_start is not None:
                new_img = self.my_image.image.copy()
                img = new_img.pillow_image()

                bigger_x, smaller_x, bigger_y, smaller_y = 0, 0, 0, 0

                if crop_start.x() >= crop_end.x():
                    bigger_x = crop_start.x()
                    smaller_x = crop_end.x()
                else:
                    bigger_x = crop_end.x()
                    smaller_x = crop_start.x()

                if crop_start.y() >= crop_end.y():
                    bigger_y = crop_start.y()
                    smaller_y = crop_end.y()
                else:
                    bigger_y = crop_end.y()
                    smaller_y = crop_start.y()

                img_left_area = (smaller_x, smaller_y, bigger_x, bigger_y)

                img_left = img.crop(img_left_area)

                new_img.set_pillow_image(img_left)

                config_window.main_window_global.draw_image(new_img)
                self.new_img = new_img

            else:
                config_window.main_window_global.draw_image(self.my_image)

    def mouseMoveEvent(self, event):
        self.curr_pointer = event.pos()

        width, height = self.my_image.dimensions

        if event.buttons() and Qt.LeftButton and self.drawing and 0 < event.pos().x() <= width and 0 < event.pos().y() <= height:
            self.crop_end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            self.handler_crop_finished()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.drawn_image)

        painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
        painter.setFont(QFont('Decorative', 20))

        # if self.curr_pointer is not None:
        #     painter.drawText(0, 40, "(" + str(self.curr_pointer.x()) + ", " + str(self.curr_pointer.y()) + ")")

        if self.crop_start is not None and self.crop_end is not None:
            painter.drawRect(self.crop_start.x(), self.crop_start.y(),
                             self.crop_end.x() - self.crop_start.x(),
                             self.crop_end.y() - self.crop_start.y())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F1:
            config_window.main_window_global.draw_image(self.my_image)
