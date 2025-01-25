import cv2
import numpy as np

class VideoProcessor:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def process_video(self, file_path, progress_callback=None):
        """
        Processes the video, detecting faces and returning processed frames.
        :param file_path: Path to the video file.
        :param progress_callback: A function to report progress (optional).
        :return: A list of processed frames.
        """
        cap = cv2.VideoCapture(file_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        processed_frames = []
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces:
                cv2.circle(frame, (x + w // 2, y + h // 2), w // 2, (0, 255, 0), 2)

            processed_frames.append(frame)
            frame_count += 1

            if progress_callback:
                progress_callback(frame_count, total_frames)

        cap.release()
        return processed_frames
