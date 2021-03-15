import os
import sys

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
    myImage: MyImage

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

        mainLayout = QHBoxLayout()

        # IMAGE 1

        # Layout for image visualization
        imagePreviewAndDataLayout = QVBoxLayout()

        self.imageLabel = QLabel(alignment=(Qt.AlignVCenter | Qt.AlignHCenter))
        self.imageLabel.setFixedSize(300, 300)
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

        # imageHeightLayout = QHBoxLayout()
        # imageHeightLayout.addWidget(QLabel("Height: ", objectName='title', alignment=Qt.AlignLeft))
        # self.imageHeightLabel = QLabel("None", alignment=Qt.AlignRight)
        # imageHeightLayout.addWidget(self.imageHeightLabel)
        # imageLabelDataLayout.addLayout(imageHeightLayout)
        #
        # imageWidthLayout = QHBoxLayout()
        # imageWidthLayout.addWidget(QLabel("Width: ", objectName='title', alignment=Qt.AlignLeft))
        # self.imageWidthLabel = QLabel("None", alignment=Qt.AlignRight)
        # imageWidthLayout.addWidget(self.imageWidthLabel)
        # imageLabelDataLayout.addLayout(imageWidthLayout)

        imageDataLayout.addLayout(imageLabelDataLayout)

        # Layout for image actions
        imageActionsLayout = QVBoxLayout()
        imageActionsLayout.setAlignment(Qt.AlignTop)
        imageActionsLayout.addWidget(QPushButton("Select image", clicked=self.selectImage))
        imageActionsLayout.addWidget(QPushButton("Convert to HSV", clicked=self.showHSV))

        pixelActionsLayout = QVBoxLayout()

        pixelInputLayout = QVBoxLayout()
        pixelXLayout = QHBoxLayout()
        pixelYLayout = QHBoxLayout()
        pixelXLabel = QLabel("X: ")
        # xIntValidator = QIntValidator(0, self.myImage.dimensions[0]) if self.myImage is not None else QIntValidator()
        self.pixelXLineEdit = QLineEdit()
        self.pixelXLineEdit.setValidator(QIntValidator())
        pixelXLayout.addWidget(pixelXLabel)
        pixelXLayout.addWidget(self.pixelXLineEdit)
        pixelYLabel = QLabel("Y: ")
        # yIntValidator = QIntValidator(0, self.myImage.dimensions[1]) if self.myImage is not None else QIntValidator()
        self.pixelYLineEdit = QLineEdit()
        self.pixelYLineEdit.setValidator(QIntValidator())
        pixelYLayout.addWidget(pixelYLabel)
        pixelYLayout.addWidget(self.pixelYLineEdit)
        pixelInputLayout.addLayout(pixelXLayout)
        pixelInputLayout.addLayout(pixelYLayout)

        getPixelLayout = QVBoxLayout()
        getPixelLayout.addWidget(QPushButton("Get pixel", clicked=self.getPixel))
        showPixelLayout = QHBoxLayout()
        showPixelTitle = QLabel("Pixel: ", alignment=Qt.AlignLeft)
        self.pixelLabel = QLabel("", alignment=Qt.AlignRight)
        showPixelLayout.addWidget(showPixelTitle)
        showPixelLayout.addWidget(self.pixelLabel)
        getPixelLayout.addLayout(showPixelLayout)

        pixelActionsLayout.addLayout(pixelInputLayout)
        pixelActionsLayout.addWidget(QPushButton("Set pixel", clicked=self.setPixel))
        pixelActionsLayout.addLayout(getPixelLayout)
        imageActionsLayout.addLayout(pixelActionsLayout)

        imageDataLayout.addLayout(imageActionsLayout)
        imagePreviewAndDataLayout.addLayout(imageDataLayout)
        mainLayout.addLayout(imagePreviewAndDataLayout)

        # Tabs
        self.tabLayout = QTabWidget()
        operationsTab = QWidget()
        operationsLayout = QHBoxLayout()
        operationsButton = QPushButton("Operations between Images", clicked=self.operationBetweenImages)
        operationsLayout.addWidget(operationsButton)
        operationsTab.setLayout(operationsLayout)

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

    def setPixel(self):
        if self.myImage is not None:
            pixel = self.askForInt("Set pixel value", 0)
            MyImage.modify_pixel(self.myImage, (self.pixelX, self.pixelY), pixel)
            self.drawImage(self.myImage)

    def showHSV(self):
        MyImage.type_conversion(self.myImage.image, Mode.HSV)

    def operationBetweenImages(self):
        if self.myImage is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('More information')
            msg.setWindowTitle("Error")
            return msg
        else:
            self.views.append(OperationsBetweenImages())

    def selectImage(self):
        options = QFileDialog.Options()
        image_path, _ = QFileDialog.getOpenFileName(self, "Select image file", "",
                                                    "Images (*.jpg *.jpeg *.raw *.pbm *.ppm *.pgm *.RAW *.png)",
                                                    options=options)
        size = self.askRawImage(image_path)
        if size:
            self.drawImage(MyImage(image_path, size))
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

    def drawImage(self, img: MyImage = None):
        if img is not None:
            self.myImage = img
            # self.imageWidthLabel.setText(str(img.dimensions[0]))
            # self.imageHeightLabel.setText(str(img.dimensions[1]))
            self.imageNameLabel.setText(img.file_name)
            self.imagePathLabel.setText(img.path)

        qim = ImageQt(self.myImage.image)
        pixmap = QPixmap.fromImage(qim).scaled(self.imageLabel.width(), self.imageLabel.height(),
                                               QtCore.Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(pixmap)

    def askForInt(self, message: str, default: int = 1, min: int = 1, max: int = 2147483647):
        intVal, _ = QInputDialog.getInt(self, "Enter integer value", message, default, min=min, max=max)
        return intVal


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
