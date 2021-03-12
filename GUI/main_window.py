import sys

from PyQt5.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog, QApplication, \
    QWidget
from PyQt5.QtCore import Qt

# Subclass QMainWindow to customise your application's main window
from TP0.image import MyImage


class MainWindow(QWidget):
    image: MyImage

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.title = 'ATI Interface'
        self.left = 200
        self.top = 100
        self.width = 1000
        self.height = 750

        self.init()
        # Force load file
        # self.selectFileButtonClicked()

        self.image = None

    def init(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # widget = QWidget()
        mainLayout = QVBoxLayout()
        imagePreviewAndDataLayout = QHBoxLayout()
        imageDataLayout = QVBoxLayout()

        fileActionsLayout = QVBoxLayout()
        fileActionsLayout.setAlignment(Qt.AlignBottom)
        fileActionsLayout.addWidget(QPushButton("Change selected file", clicked=self.selectFileButtonClicked))

        imageDataLayout.addLayout(fileActionsLayout)
        imagePreviewAndDataLayout.addLayout(imageDataLayout)
        mainLayout.addLayout(imagePreviewAndDataLayout)

        self.setLayout(mainLayout)
        # self.setCentralWidget(widget)
        self.show()

    def selectFileButtonClicked(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select image file", "",
                                                   "Images (*.jpg *.jpeg *.raw *.ppm *.pgm *.RAW *.png)",
                                                   options=options)
        if file_path:
            self.loadImage(MyImage.load_image(file_path))
            return True
        return False

    def loadImage(self, img: MyImage = None):
        if img is not None:
            self.image = img


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    # Force load file
    mainWindow.selectFileButtonClicked()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
