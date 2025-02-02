from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class BoundingBoxWidget(QDialog):
    def __init__(self, bounding_box, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bounding Box Coordinates")
        self.setGeometry(300, 300, 300, 200)
        layout = QVBoxLayout()

        self.left_input = QLineEdit(str(bounding_box[0]))
        self.top_input = QLineEdit(str(bounding_box[1]))
        self.right_input = QLineEdit(str(bounding_box[0] + bounding_box[2]))
        self.bottom_input = QLineEdit(str(bounding_box[1] + bounding_box[3]))

        layout.addWidget(QLabel("Left:"))
        layout.addWidget(self.left_input)
        layout.addWidget(QLabel("Top:"))
        layout.addWidget(self.top_input)
        layout.addWidget(QLabel("Right:"))
        layout.addWidget(self.right_input)
        layout.addWidget(QLabel("Bottom:"))
        layout.addWidget(self.bottom_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_bbox)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
        self.bounding_box = bounding_box

    def submit_bbox(self):
        try:
            x = int(self.left_input.text())
            y = int(self.top_input.text())
            w = int(self.right_input.text()) - x
            h = int(self.bottom_input.text()) - y
            self.bounding_box = (x, y, w, h)
            self.accept()  
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid integer values.")
