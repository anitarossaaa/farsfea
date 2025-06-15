from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self, login_callback):
        super().__init__()
        self.login_callback = login_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Header
        header = QHBoxLayout()
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #2ecc71;")
        header_frame.setFixedHeight(50)

        title = QLabel("FARSFEA")
        title.setStyleSheet("font-weight: bold; font-size: 18px; margin-left: 10px;")
        login_btn = QPushButton("ADMIN LOGIN")
        login_btn.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; padding: 5px 18px; border-radius: 6px;")
        login_btn.clicked.connect(self.login_callback)

        h_layout = QHBoxLayout(header_frame)
        h_layout.addWidget(title)
        h_layout.addStretch()
        h_layout.addWidget(login_btn)

        layout.addWidget(header_frame)

        # Title
        page_title = QLabel("Face Recognition System for Employee Attendance")
        page_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 15px;")
        page_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(page_title)

        # Placeholder box
        box = QFrame()
        box.setStyleSheet("background-color: #f0f0f0; border: 1px solid black;")
        box.setFixedSize(600, 300)
        layout.addWidget(box, alignment=Qt.AlignCenter)

        # Dynamic label
        label = QLabel("Real-time face detection (Tanggal & waktu dinamis di sini)")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.setLayout(layout)
