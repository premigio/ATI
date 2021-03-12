import os
import sys

from PIL.ImageQt import ImageQt
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog, QApplication, \
    QWidget, QInputDialog, QTabWidget
from PyQt5.QtCore import Qt

# Subclass QMainWindow to customise your application's main window
from GUI.image_window import ImageWindow
from GUI.operations_window import OperationsBetweenImages
from TP0.image import MyImage, Mode
from TP0.main import sizeDict


class MainWindow(QWidget):
    image: MyImage

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.title = 'ATI Interface'
        self.left = 200
        self.top = 100
        self.width = 1000
        self.height = 750
        self.image = None

        self.set_layouts()

        self.views = []

    def set_layouts(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        mainLayout = QVBoxLayout()

        # IMAGE 1

        # Layout for image visualization
        imagePreviewAndDataLayout = QHBoxLayout()

        self.imageLabel = QLabel(alignment=(Qt.AlignVCenter | Qt.AlignHCenter))
        self.imageLabel.setFixedSize(400, 400)
        self.imageLabel.setStyleSheet(
            "QLabel { border-style: solid; border-width: 2px; border-color: rgba(0, 0, 0, 0.1); }")
        imagePreviewAndDataLayout.addWidget(self.imageLabel)

        # Layout for image data
        imageDataLayout = QVBoxLayout()

        imageLabelDataLayout = QVBoxLayout()
        imageLabelDataLayout.setAlignment(Qt.AlignTop)

        imageLabelLayout = QHBoxLayout()
        imageLabelLayout.addWidget(QLabel("Name: ", objectName='title', alignment=Qt.AlignLeft))
        self.imageNameLabel = QLabel("None", alignment=Qt.AlignRight)
        imageLabelLayout.addWidget(self.imageNameLabel)
        imageLabelDataLayout.addLayout(imageLabelLayout)

        imageDirLayout = QHBoxLayout()
        imageDirLayout.addWidget(QLabel("Path: ", objectName='title', alignment=Qt.AlignLeft))
        self.imagePathLabel = QLabel("None", alignment=Qt.AlignRight)
        imageDirLayout.addWidget(self.imagePathLabel)
        imageLabelDataLayout.addLayout(imageDirLayout)

        imageHeightLayout = QHBoxLayout()
        imageHeightLayout.addWidget(QLabel("Height: ", objectName='title', alignment=Qt.AlignLeft))
        self.imageHeightLabel = QLabel("None", alignment=Qt.AlignRight)
        imageHeightLayout.addWidget(self.imageHeightLabel)
        imageLabelDataLayout.addLayout(imageHeightLayout)

        imageWidthLayout = QHBoxLayout()
        imageWidthLayout.addWidget(QLabel("Width: ", objectName='title', alignment=Qt.AlignLeft))
        self.imageWidthLabel = QLabel("None", alignment=Qt.AlignRight)
        imageWidthLayout.addWidget(self.imageWidthLabel)
        imageLabelDataLayout.addLayout(imageWidthLayout)

        imageDataLayout.addLayout(imageLabelDataLayout)

        # Layout for image actions
        imageActionsLayout = QVBoxLayout()
        imageActionsLayout.setAlignment(Qt.AlignTop)
        imageActionsLayout.addWidget(QPushButton("Select image", clicked=self.selectImage))
        imageActionsLayout.addWidget(QPushButton("Convert to HSV", clicked=self.showHSV))
        imageActionsLayout.addWidget(QPushButton("Get pixel", clicked=self.getPixel))
        self.pixelLabel = QLabel("None", alignment=Qt.AlignRight)
        imageActionsLayout.addWidget(self.pixelLabel)
        imageActionsLayout.addWidget(QPushButton("Set pixel", clicked=self.setPixel))

        imageDataLayout.addLayout(imageActionsLayout)
        imagePreviewAndDataLayout.addLayout(imageDataLayout)
        mainLayout.addLayout(imagePreviewAndDataLayout)

        # Tabs
        self.tabLayout = QTabWidget()
        operationsTab = QWidget()
        operationsLayout = QHBoxLayout()
        operationsButton = QPushButton("Operations between Images")
        operationsButton.clicked.connect(self.operation_between_images)
        operationsLayout.addWidget(operationsButton)
        operationsTab.setLayout(operationsLayout)

        generatorTab = QWidget()
        generatorTab = QWidget()
        sideActionsLayout = QVBoxLayout()
        sideActionsLayout.setAlignment(Qt.AlignCenter)
        sideActionsLayout.addWidget(QPushButton("Generate square image", clicked=self.showSquare))
        sideActionsLayout.addWidget(QPushButton("Generate circle image", clicked=self.showCircle))
        generatorTab.setLayout(sideActionsLayout)

        self.tabLayout.addTab(operationsTab, "Operations")
        self.tabLayout.addTab(generatorTab, "Generator")
        mainLayout.addWidget(self.tabLayout)

        self.setLayout(mainLayout)
        self.show()

    def showSquare(self):
        MyImage.create_square_image().show()

    def showCircle(self):
        MyImage.create_circle_image().show()

    def getPixel(self):
        pixel_x = self.askForInt("Enter X coordinate", 0)
        pixel_y = self.askForInt("Enter Y coordinate", 0)
        pixel = MyImage.get_pixel(self.image.image, (pixel_x, pixel_y))
        if pixel:
            self.pixelLabel.setText(str(pixel))

    def setPixel(self):
        pixel_x = self.askForInt("Enter X coordinate", 0)
        pixel_y = self.askForInt("Enter Y coordinate", 0)
        pixel = self.askForInt("Set pixel value", 0)
        MyImage.modify_pixel(self.image, (pixel_x, pixel_y), pixel)

    def showHSV(self):
        MyImage.type_conversion(self.image.image, Mode.HSV)

    def operation_between_images(self):
        self.views.append(OperationsBetweenImages())

    def selectImage(self):
        options = QFileDialog.Options()
        image_path, _ = QFileDialog.getOpenFileName(self, "Select image file", "",
                                                    "Images (*.jpg *.jpeg *.raw *.pbm *.ppm *.pgm *.RAW *.png)",
                                                    options=options)
        size = self.askRawImage(image_path)
        if size:
            self.loadImage(MyImage(image_path, size))
            return True
        return False

    def askRawImage(self, image_path):
        if image_path:
            fileextension = os.path.splitext(image_path)[1]
            if fileextension == ".raw" or fileextension == ".RAW":
                width = self.askForInt("Enter image width", 256)
                height = self.askForInt("Enter image height", 256)
                return width, height
        return None

    def loadImage(self, img: MyImage = None):
        if img is not None:
            self.image = img
            self.imageWidthLabel.setText(str(img.dimensions[0]))
            self.imageHeightLabel.setText(str(img.dimensions[1]))
            self.imageNameLabel.setText(img.file_name)
            self.imagePathLabel.setText(img.path)

        qim = ImageQt(self.image.image)
        pixmap = QPixmap.fromImage(qim).scaled(self.imageLabel.width(), self.imageLabel.height(),
                                               QtCore.Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(pixmap)

    def askForInt(self, message: str, default: int = 1, min: int = 1, max: int = 2147483647):
        intVal, _ = QInputDialog.getInt(self, "Enter integer value", message, default, min=min, max=max)
        return intVal


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()

    # Force load file
    if not main_window.selectImage():
        return

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
