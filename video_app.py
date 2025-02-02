import cv2
import numpy as np
from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMessageBox, QSizePolicy
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer, Qt
from model import FaceDetector
from bounding_box_widget import BoundingBoxWidget


class VideoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Detection Video App")
        self.setGeometry(100, 100, 900, 700)

        self.detector = FaceDetector()
        self.cap = None
        self.bounding_box = None
        self.userbbox = None
        self.is_paused = False
        self.largest_bbox = None  

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()

        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.video_label.setStyleSheet("background-color: black;")
        main_layout.addWidget(self.video_label)

        playback_layout = QHBoxLayout()
        self.backward_button = QPushButton("⏪ Backward")
        self.backward_button.clicked.connect(self.skip_backward)
        playback_layout.addWidget(self.backward_button)

        self.pause_button = QPushButton("⏸ Pause")
        self.pause_button.clicked.connect(self.toggle_pause)
        playback_layout.addWidget(self.pause_button)

        self.forward_button = QPushButton("⏩ Forward")
        self.forward_button.clicked.connect(self.skip_forward)
        playback_layout.addWidget(self.forward_button)

        self.open_video_button = QPushButton("Open Video")
        self.open_video_button.clicked.connect(self.open_video)
        playback_layout.addWidget(self.open_video_button)

        self.largest_bbox_button = QPushButton("Find Largest Bounding Box")
        self.largest_bbox_button.clicked.connect(self.find_largest_bounding_box)
        playback_layout.addWidget(self.largest_bbox_button)

        main_layout.addLayout(playback_layout)

        self.central_widget.setLayout(main_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def open_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi)")
        if file_path:
            self.cap = cv2.VideoCapture(file_path)
            if not self.cap.isOpened():
                QMessageBox.critical(self, "Error", "Cannot open video file!")
                return
            self.timer.start(30)

    def toggle_pause(self):
        if self.cap:
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.timer.stop()
                self.pause_button.setText("▶ Play")
                if self.bounding_box is not None:
                    self.show_bbox_widget()
            else:
                self.timer.start(30)
                self.pause_button.setText("⏸ Pause")

    def skip_forward(self):
        if self.cap:
            current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            new_frame = min(current_frame + 1, total_frames - 1)  
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            self.update_frame()  

    def skip_backward(self):
        if self.cap:
            current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            new_frame = max(current_frame - 1, 0)  
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            self.update_frame()  

    def update_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                processed_frame, bbox = self.detector.process_frame(frame)

                if bbox is not None and len(bbox) == 4:
                    self.bounding_box = bbox
                    if self.userbbox is not None and len(self.userbbox) == 4:
                        bbox = self.userbbox
                    x, y, w, h = bbox
                    corners = {
                        "Top Left": (x, y),
                        "Top Right": (x + w, y),
                        "Bottom Left": (x, y + h),
                        "Bottom Right": (x + w, y + h),
                    }

                    cv2.rectangle(processed_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    for label, (cx, cy) in corners.items():
                        cv2.putText(processed_frame, f"({cx}, {cy})", (cx, cy - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2, cv2.LINE_AA)

                self.display_frame(processed_frame)
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  
                if not self.is_paused:
                    self.timer.start(30)  

    def display_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        qimg = QImage(frame.data, w, h, ch * w, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.video_label.setPixmap(pixmap.scaled(self.video_label.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def show_bbox_widget(self):
        if self.bounding_box is not None and len(self.bounding_box) > 0:
            self.bbox_widget = BoundingBoxWidget(self.bounding_box, self)
            self.bbox_widget.exec()
            self.userbbox = self.bbox_widget.bounding_box

    def find_largest_bounding_box(self):
        if self.cap is None or not self.cap.isOpened():
            QMessageBox.warning(self, "Warning", "No video is loaded!")
            return

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.largest_bbox = None
        max_area = 0

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break  

            _, bbox = self.detector.process_frame(frame)
            if bbox is not None and len(bbox) == 4:
                x, y, w, h = bbox
                area = w * h  
                if area > max_area:
                    max_area = area
                    self.largest_bbox = bbox

        if self.largest_bbox is not None:
            with open("largest_bbox_coordinates.txt", "w") as file:
                file.write(f"Largest Bounding Box Coordinates: {self.largest_bbox}\n")
                #file.write(f"Area: {max_area}\n")  /*uncomment to fing the area of largest bounding box**/
            QMessageBox.information(self, "Success", "Largest bounding box coordinates saved to 'largest_bbox_coordinates.txt'!")
        else:
            QMessageBox.warning(self, "Warning", "No bounding boxes found in the video!")