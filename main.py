import sys
from PyQt6.QtWidgets import QApplication
from video_app import VideoApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoApp()
    window.show()
    sys.exit(app.exec())
