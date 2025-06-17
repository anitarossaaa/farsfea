from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QTableWidget, QTableWidgetItem, QAbstractItemView, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPainter, QBrush
from ui.navbar import Navbar

class AdminHapusKaryawan(QWidget):
    def __init__(self, username, logout_callback, menu_callbacks):
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

        # Body
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar/navbar
        navbar = Navbar(self.menu_callbacks)
        body_layout.addWidget(navbar)

        # Main content
        main_content = QFrame()
        main_content.setStyleSheet("background-color: white;")
        main_content_layout = QVBoxLayout(main_content)
        main_content_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_label.setStyleSheet("font-size: 15px; font-weight: normal;")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari nama/NIK karyawan")
        self.search_input.setFixedWidth(250)
        search_btn = QPushButton()
        search_btn.setFixedWidth(34)
        search_btn.setIcon(QIcon.fromTheme("search"))  # icon system, fallback nanti
        search_btn.setStyleSheet("background-color: #fff; border: 1px solid #aaa;")

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        search_layout.addStretch()
        main_content_layout.addLayout(search_layout)
        main_content_layout.addSpacing(15)

        # Tabel data
        table = QTableWidget(1, 4)  # 1 contoh baris, 4 kolom
        table.setHorizontalHeaderLabels(["NIK", "Nama", "Foto", "Action"])
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.NoSelection)
        table.setFixedWidth(600)
        table.setFixedHeight(120)
        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setVisible(False)

        # Baris contoh
        table.setItem(0, 0, QTableWidgetItem("123"))
        table.setItem(0, 1, QTableWidgetItem("Bram"))

        # Placeholder gambar
        foto_label = QLabel()
        foto_pixmap = QPixmap(40, 40)
        foto_pixmap.fill(QColor('gray'))
        foto_label.setPixmap(foto_pixmap)
        foto_label.setAlignment(Qt.AlignCenter)
        table.setCellWidget(0, 2, foto_label)

        # Tombol hapus bulat merah dengan icon silang putih
        hapus_btn = QPushButton()
        hapus_btn.setFixedSize(30, 30)
        hapus_btn.setStyleSheet(
            "background-color: #e74c3c; border-radius: 15px;"
            "color: white; font-size: 18px; font-weight: bold;"
        )
        # Gambar icon silang putih secara custom
        hapus_btn.setIcon(self.make_cross_icon())
        hapus_btn.setIconSize(foto_pixmap.rect().size())
        table.setCellWidget(0, 3, hapus_btn)

        main_content_layout.addWidget(table, alignment=Qt.AlignHCenter)
        body_layout.addWidget(main_content)
        layout.addLayout(body_layout)
        self.setLayout(layout)

    def make_cross_icon(self):
        """Return QIcon with white cross in a transparent square"""
        pm = QPixmap(18, 18)
        pm.fill(Qt.transparent)
        painter = QPainter(pm)
        pen = painter.pen()
        pen.setColor(Qt.white)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawLine(4, 4, 14, 14)
        painter.drawLine(4, 14, 14, 4)
        painter.end()
        return QIcon(pm)
