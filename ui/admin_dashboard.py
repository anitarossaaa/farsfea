from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt
from ui.navbar import Navbar

class AdminDashboard(QWidget):
    def __init__(self, username, logout_callback, menu_callbacks):
        """
        username: str, nama user login
        logout_callback: fungsi jika logout
        menu_callbacks: dict, key = menu, value = callback function
        """
        super().__init__()
        self.username = username
        self.logout_callback = logout_callback
        self.menu_callbacks = menu_callbacks
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #a5d6a7;")
        header_frame.setFixedHeight(50)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 0, 10, 0)

        title = QLabel("FARSFEA")
        title.setStyleSheet("font-weight: bold; font-size: 20px;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        logout_btn = QPushButton("LOG OUT")
        logout_btn.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold; padding: 5px 18px; border-radius: 6px;")
        logout_btn.clicked.connect(self.logout_callback)
        header_layout.addWidget(logout_btn)

        layout.addWidget(header_frame)

        # Body: Sidebar + Main
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar/navbar (modular)
        navbar = Navbar(self.menu_callbacks)
        body_layout.addWidget(navbar)

        # Main content
        main_content = QFrame()
        main_content.setStyleSheet("background-color: white;")
        main_content_layout = QVBoxLayout(main_content)
        main_content_layout.setAlignment(Qt.AlignCenter)

        welcome_label = QLabel(f"Selamat datang di\nFARSFEA, {self.username}")
        welcome_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        welcome_label.setAlignment(Qt.AlignCenter)
        main_content_layout.addWidget(welcome_label)

        body_layout.addWidget(main_content)

        layout.addLayout(body_layout)
        self.setLayout(layout)
