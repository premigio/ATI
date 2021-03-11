from PyQt5.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt


# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.title = 'ATI Interface'
        self.left = 200
        self.top = 100
        self.width = 1000
        self.height = 750
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.mainLayout()

        label = QLabel("This is a PyQt5 window!")

        # The `Qt` namespace has a lot of attributes to customise
        # widgets. See: http://doc.qt.io/qt-5/qt.html
        label.setAlignment(Qt.AlignCenter)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(label)

    def mainLayout(self):
        mainLayout = QVBoxLayout()

        self.setLayout(mainLayout)
        self.show()