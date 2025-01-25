from PySide6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QSlider, 
                               QVBoxLayout, QWidget, QStyle, QPushButton, QLabel, QHBoxLayout, QMenuBar)
from PySide6.QtMultimedia import QMediaPlayer, QVideoSink
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QImage, QPixmap, QPainter
import sys
import cv2
import numpy as np


class ImageFaceDetector(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Face Detector")
        self.setGeometry(100, 100, 800, 600)

        # Create Widgets
        self.imageLabel = QLabel("Open an image to detect faces")
        self.imageLabel.setAlignment(Qt.AlignCenter)

        # Buttons
        self.openButton = QPushButton("Open Image")
        self.openButton.clicked.connect(self.open_file)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.imageLabel)
        layout.addWidget(self.openButton)

        # Central Widget
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        # Menu Bar
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)

        fileMenu = menuBar.addMenu("File")
        openAction = fileMenu.addAction("Open")
        openAction.triggered.connect(self.open_file)

        closeAction = fileMenu.addAction("Close")
        closeAction.triggered.connect(self.close_application)

        # Face Cascade
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def open_file(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if filePath:
            self.detect_faces(filePath)

    def detect_faces(self, filePath):
        # Load the image
        image = cv2.imread(filePath)
        if image is None:
            self.statusBar().showMessage("Failed to load image")
            return

        # Convert image to grayscale for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw circles around the detected faces
        for (x, y, w, h) in faces:
            center = (x + w // 2, y + h // 2)
            radius = w // 2
            cv2.circle(image, center, radius, (0, 255, 0), 2)

        # Convert the image back to RGB for display
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Display the result in the QLabel
        self.imageLabel.setPixmap(QPixmap.fromImage(q_image))
        self.imageLabel.setScaledContents(True)

    def close_application(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageFaceDetector()
    window.show()
    sys.exit(app.exec())
