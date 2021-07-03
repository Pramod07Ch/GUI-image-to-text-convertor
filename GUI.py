import sys
import os
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QPushButton, QFileDialog, QWidget, QCheckBox, QHBoxLayout

# User defined imports
from image_to_text import OCRReader


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.image_path = None
        self.display_bg = True
        self.display_image = True

        self.initUI()

    def initUI(self):
        self.setWindowTitle("OCR Reader")

        bg_box = QCheckBox("Display Background")
        bg_box.setChecked(True)
        bg_box.stateChanged.connect(lambda: self.bg_state(bg_box))
        image_box = QCheckBox("Display Image")
        image_box.setChecked(True)
        image_box.stateChanged.connect(lambda: self.image_state(image_box))
        upload_button = QPushButton("Upload Image", self)
        upload_button.clicked.connect(self.upload_image)
        reconvert_button = QPushButton("Re-Convert", self)
        reconvert_button.clicked.connect(self.convert_image_to_text)

        widget = QWidget()
        h_layout = QHBoxLayout()
        h_layout.addStretch(1)
        h_layout.addWidget(bg_box)
        h_layout.addWidget(image_box)

        v_layout = QVBoxLayout()
        v_layout.addStretch(1)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(upload_button)
        v_layout.addWidget(reconvert_button)
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)

    def upload_image(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "Select image", os.getenv("HOME"), "(*.png *.xpm .jpg)")
        if image_path != "":
            self.image_path = image_path
            self.convert_image_to_text()

    def convert_image_to_text(self):
        if self.image_path is not None:
            OCRReader(self.image_path, self.display_bg, self.display_image)
        else:
            print("Please select an image file first!")

    def bg_state(self, button):
        self.display_bg = True if button.isChecked() else False

    def image_state(self, button):
        self.display_image = True if button.isChecked() else False


if __name__ == "__main__":
    ocr_app = QApplication(sys.argv)
    ocr_app.setStyle("Fusion")
    gui = MainWindow()
    gui.show()
    sys.exit(ocr_app.exec_())