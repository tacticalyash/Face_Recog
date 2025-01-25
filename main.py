from PySide6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QSlider,
                               QVBoxLayout, QWidget, QStyle, QPushButton, QLabel, QHBoxLayout, QMenuBar, QProgressBar)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
import sys
from model import VideoProcessor


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PySide6 Video Player")
        self.setGeometry(100, 100, 800, 600)

        self.videoProcessor = VideoProcessor()
        self.videoWidget = QLabel()
        self.videoWidget.setAlignment(Qt.AlignCenter)
        self.videoWidget.setStyleSheet("background-color: black;")

        self.playButton = QPushButton()
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.toggle_playback)
        self.playButton.setEnabled(False)

        self.forwardButton = QPushButton("Forward>>")
        self.forwardButton.clicked.connect(self.forward_video)
        self.forwardButton.setEnabled(False)

        self.backwardButton = QPushButton("<<Backward")
        self.backwardButton.clicked.connect(self.backward_video)
        self.backwardButton.setEnabled(False)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.set_position)

        self.labelDuration = QLabel("00:00 / 00:00")
        self.progressBar = QProgressBar()
        self.progressBar.setVisible(False)

        controlLayout = QHBoxLayout()
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.backwardButton)
        controlLayout.addWidget(self.forwardButton)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.labelDuration)

        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)
        layout.addWidget(self.progressBar)
        layout.addLayout(controlLayout)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)

        fileMenu = menuBar.addMenu("File")
        openAction = fileMenu.addAction("Open")
        openAction.triggered.connect(self.open_file)

        closeAction = fileMenu.addAction("Close")
        closeAction.triggered.connect(self.close_video)

        self.processed_frames = []
        self.frame_index = 0
        self.play_timer = QTimer()
        self.play_timer.timeout.connect(self.play_frame)

    def open_file(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi *.mkv *.mov *.flv)")
        if filePath:
            self.progressBar.setVisible(True)
            self.process_video(filePath)

    def process_video(self, filePath):
        def update_progress(current, total):
            self.progressBar.setValue(int((current / total) * 100))
            QApplication.processEvents()

        self.processed_frames = self.videoProcessor.process_video(filePath, update_progress)
        self.progressBar.setVisible(False)
        self.statusBar().showMessage("Video processing completed.")
        self.playButton.setEnabled(True)
        self.forwardButton.setEnabled(True)
        self.backwardButton.setEnabled(True)
        self.start_playback()

    def start_playback(self):
        self.frame_index = 0
        self.positionSlider.setRange(0, len(self.processed_frames) - 1)
        self.play_timer.start(30)

    def play_frame(self):
        if self.frame_index < len(self.processed_frames):
            frame = self.processed_frames[self.frame_index]
            self.display_frame(frame)
            self.frame_index += 1
            self.positionSlider.setValue(self.frame_index)
            self.update_duration_label()
        else:
            self.play_timer.stop()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def display_frame(self, frame):
        height, width, _ = frame.shape
        qimg = QImage(frame.data, width, height, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(qimg)
        self.videoWidget.setPixmap(pixmap)

    def close_video(self):
        self.play_timer.stop()
        self.processed_frames = []
        self.videoWidget.clear()
        self.positionSlider.setValue(0)
        self.labelDuration.setText("00:00 / 00:00")
        self.playButton.setEnabled(False)
        self.forwardButton.setEnabled(False)
        self.backwardButton.setEnabled(False)

    def toggle_playback(self):
        if self.play_timer.isActive():
            self.play_timer.stop()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.play_timer.start(30)
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

    def set_position(self, position):
        self.frame_index = position
        self.display_frame(self.processed_frames[self.frame_index])

    def forward_video(self):
        jump_frames = 30 * 5 
        self.frame_index = min(self.frame_index + jump_frames, len(self.processed_frames) - 1)
        self.display_frame(self.processed_frames[self.frame_index])
        self.positionSlider.setValue(self.frame_index)
        self.update_duration_label()

    def backward_video(self):
        jump_frames = 30 * 5 
        self.frame_index = max(self.frame_index - jump_frames, 0)
        self.display_frame(self.processed_frames[self.frame_index])
        self.positionSlider.setValue(self.frame_index)
        self.update_duration_label()

    def update_duration_label(self):
        total_frames = len(self.processed_frames)
        current_time = f"{self.frame_index // 30:02}:{self.frame_index % 30:02}"
        total_time = f"{total_frames // 30:02}:{total_frames % 30:02}"
        self.labelDuration.setText(f"{current_time} / {total_time}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec())
