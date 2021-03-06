from PIL.ImageQt import ImageQt
from PyQt5 import QtCore
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont
from PyQt5.QtWidgets import QWidget, QLabel, QDesktopWidget
from PyQt5.QtCore import Qt

from GUI import config_window, crop_image_utils
from Algorithms.Classes.MyImage import MyImage


class ImageCropper(QWidget):
    def __init__(self, image: MyImage):
        super().__init__()
        self.my_image = image
        self.image_label = QLabel(alignment=(Qt.AlignVCenter | Qt.AlignHCenter))
        qim = ImageQt(self.my_image.image)
        pixmap = QPixmap.fromImage(qim).scaled(self.image_label.width(), self.image_label.width(),
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

                img_left = crop_image_utils.get_cropped_image(img, self.get_crop())

                new_img.set_pillow_image(img_left)

                config_window.main_window_global.draw_image(new_img)

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