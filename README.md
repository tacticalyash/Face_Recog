# Face Detection Video Player

Face Detection Video Player is a Python-based application that combines video playback functionality with real-time face detection. It provides a sleek interface, similar to VLC, for video navigation and processing each frame for face detection using machine learning.

## Features

- **Video Playback**: Play, pause, skip forward, and backward.
- **Face Detection**: Real-time face detection on video frames.
- **User-Friendly UI**: Built with Qt for a modern and responsive interface.
- **Model**: used Haar Cascade Classifiers for real-time face detection, which is pre-trained and highly optimized for performance.

## Installation

Follow these steps to set up the application:
1) Clone the repository .
2) Install the Python 3.7 > .
3) Run the pip install -r requirements.txt in the project folder.


### Prerequisites
- Python 3.7 or above
- Virtual environment (optional but recommended)
- [Qt for Python](https://doc.qt.io/qtforpython/)
- opencv-python
- PyQt6

#### Execution / Usage
1) Run the "main.py" 
2) Open the video by clicking menu button (You can import video  from Video_samples folder.) e.g ->https://www.youtube.com/watch?v=8R7XqslaEUE
3) After importing the video it will start processing the video then it will take specific time to process
4) Green circle will shown on Face . It will only detect the Larger face with coordinates.(Multiple face)
5) Press the Pause button , Bounding Box widget will open , Modify the values then it will show the updated one.
6) Click the Find Largest bounding box , it will generate the text with writes the coordinates and area.

#### 
