import cv2

class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            return frame, None  

        largest_face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = largest_face

        # uncomment this to show the real time bounding box
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return frame, largest_face
