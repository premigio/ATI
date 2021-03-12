import os

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QInputDialog

from GUI.multiple_images import MultipleImageSelector
from TP0.image import MyImage


class OperationsBetweenImages(QWidget):
    def __init__(self):
        super().__init__()

        self.select_images_btn = None
        self.product_btn = None
        self.addition_btn = None
        self.subtraction_btn = None
        self.first_image = None
        self.second_image = None
        self.result_widget = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Operations between two images")

        layout = QVBoxLayout()

        first_layout = QHBoxLayout()

        self.select_images_btn = QPushButton("Select images")
        self.select_images_btn.clicked.connect(self.select_images)

        first_layout.addWidget(self.select_images_btn)

        layout.addLayout(first_layout)

        second_layout = QHBoxLayout()

        self.product_btn = QPushButton("Product")
        # self.product_btn.clicked.connect(self.product)

        second_layout.addWidget(self.product_btn)

        self.addition_btn = QPushButton("Addition")
        # self.addition_btn.clicked.connect(self.addition)

        second_layout.addWidget(self.addition_btn)

        self.subtraction_btn = QPushButton("Subtraction")
        # self.subtraction_btn.clicked.connect(self.subtraction)

        second_layout.addWidget(self.subtraction_btn)

        layout.addLayout(second_layout)

        self.setLayout(layout)
        self.show()

        self.set_enabled_operations(False)

    def select_images(self):
        def handler(paths):
            first_size = self.askRawImage(paths[0])
            if first_size:
                self.first_image = MyImage(paths[0], first_size)
            second_size = self.askRawImage(paths[1])
            if second_size:
                self.second_image = MyImage(paths[1], second_size)
        self.set_enabled_operations(True)
        self.select_images_btn.setEnabled(False)

        MultipleImageSelector(["First image", "Second image"], "Submit",
                              "Images selection", handler)

    def set_enabled_operations(self, enabled):
        for btn in [self.product_btn, self.subtraction_btn, self.addition_btn]:
            btn.setEnabled(enabled)

    def askRawImage(self, image_path):
        if image_path:
            fileextension = os.path.splitext(image_path)[1]
            if fileextension == ".raw" or fileextension == ".RAW":
                width = self.askForInt("Enter image width", 256)
                height = self.askForInt("Enter image height", 256)
                return width, height
        return None

    def askForInt(self, message: str, default: int = 1, min: int = 1, max: int = 2147483647):
        intVal, _ = QInputDialog.getInt(self, "Enter integer value", message, default, min=min, max=max)
        return intVal