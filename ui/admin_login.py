from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QMessageBox
from PyQt5.QtCore import Qt
from data.database import verify_login

class AdminLogin(QWidget):
    def __init__(self, back_callback, dashboard_callback):
        super().__init__()
        self.back_callback = back_callback
        self.dashboard_callback = dashboard_callback
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
        back_btn = QPushButton("BACK")
        back_btn.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold; padding: 5px 18px; border-radius: 6px;")
        back_btn.clicked.connect(self.back_callback)

        h_layout = QHBoxLayout(header_frame)
        h_layout.addWidget(title)
        h_layout.addStretch()
        h_layout.addWidget(back_btn)

        layout.addWidget(header_frame)

        # Form
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)

        label = QLabel("Admin Login")
        label.setStyleSheet("font-size: 24px; font-weight: bold;")
        form_layout.addWidget(label)

        username_label = QLabel("USERNAME")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Masukkan username")
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)

        password_label = QLabel("PASSWORD")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)

        login_btn = QPushButton("LOGIN")
        login_btn.setStyleSheet("background-color: #3498db; color: white;")
        login_btn.clicked.connect(self.handle_login)  # <--- Panggil handle_login saat klik
        form_layout.addWidget(login_btn)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if verify_login(username, password):
            QMessageBox.information(self, "Login Sukses", "Login admin berhasil!")
            self.dashboard_callback(username)
        else:
            QMessageBox.warning(self, "Login Gagal", "Username atau password salah.")
