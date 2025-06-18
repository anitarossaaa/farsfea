from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QTableWidget, QTableWidgetItem, QAbstractItemView
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon, QPixmap, QPainter

from ui.navbar import Navbar

DUMMY_KARYAWAN = [
    {"nik": f"{1000 + i}", "nama": f"Nama Karyawan {i+1}"}
    for i in range(40)
]
ROWS_PER_PAGE = 10

class AdminTampilkanDataKaryawan(QWidget):
    def __init__(self, username, logout_callback, menu_callbacks, page=1):
        super().__init__()
        self.username = username
        self.logout_callback = logout_callback
        self.menu_callbacks = menu_callbacks
        self.page = page
        self.total_pages = ((len(DUMMY_KARYAWAN) - 1) // ROWS_PER_PAGE) + 1

        # --- SETUP LAYOUT SEKALI ---
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

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

        self.layout.addWidget(header_frame)

        # Body
        self.body_layout = QHBoxLayout()
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addLayout(self.body_layout)

        # Sidebar/navbar
        navbar = Navbar(self.menu_callbacks)
        self.body_layout.addWidget(navbar)

        # Main content area (isi akan diisi/di-refresh)
        self.main_content = QFrame()
        self.main_content.setStyleSheet("background-color: white;")
        self.body_layout.addWidget(self.main_content)

        self.refresh_main_content()

    def refresh_main_content(self):
        # Hapus layout dan widget lama di main_content
        old_layout = self.main_content.layout()
        if old_layout:
            while old_layout.count():
                item = old_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            QWidget().setLayout(old_layout)

        main_content_layout = QVBoxLayout()
        main_content_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.main_content.setLayout(main_content_layout)

        # Judul
        title_label = QLabel("DATA KARYAWAN")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 15px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_content_layout.addWidget(title_label)
        main_content_layout.addSpacing(10)

        # Data untuk halaman ini
        start = (self.page - 1) * ROWS_PER_PAGE
        end = min(start + ROWS_PER_PAGE, len(DUMMY_KARYAWAN))
        page_data = DUMMY_KARYAWAN[start:end]

        table = QTableWidget(len(page_data), 3)
        table.setHorizontalHeaderLabels(["No.", "NIK", "Nama"])
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.NoSelection)
        table.setFixedWidth(600)
        table.setFixedHeight(260)
        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setVisible(False)
        for i, row in enumerate(page_data):
            table.setItem(i, 0, QTableWidgetItem(str(start + i + 1)))
            table.setItem(i, 1, QTableWidgetItem(row["nik"]))
            table.setItem(i, 2, QTableWidgetItem(row["nama"]))

        main_content_layout.addWidget(table, alignment=Qt.AlignHCenter)

        # Pagination
        pagination_layout = QHBoxLayout()
        page_info = QLabel(f"Showing page {self.page} of {self.total_pages}")
        pagination_layout.addWidget(page_info)
        pagination_layout.addStretch()

        prev_btn = QPushButton()
        prev_btn.setFixedSize(32, 32)
        prev_btn.setIcon(self.make_arrow_icon(left=True))
        prev_btn.setStyleSheet("background-color: #4285f4; border-radius: 16px;")
        prev_btn.clicked.connect(self.prev_page)

        next_btn = QPushButton()
        next_btn.setFixedSize(32, 32)
        next_btn.setIcon(self.make_arrow_icon(left=False))
        next_btn.setStyleSheet("background-color: #4285f4; border-radius: 16px;")
        next_btn.clicked.connect(self.next_page)

        # Enable/disable tombol agar lebih user-friendly
        prev_btn.setEnabled(self.page > 1)
        next_btn.setEnabled(self.page < self.total_pages)

        pagination_layout.addWidget(prev_btn)
        pagination_layout.addWidget(next_btn)
        main_content_layout.addLayout(pagination_layout)

    def make_arrow_icon(self, left=True):
        pm = QPixmap(18, 18)
        pm.fill(Qt.transparent)
        painter = QPainter(pm)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.white)
        painter.setBrush(Qt.white)
        if left:
            points = [
                pm.rect().center() + QPoint(-4, 0),
                pm.rect().center() + QPoint(3, -6),
                pm.rect().center() + QPoint(3, 6)
            ]
        else:
            points = [
                pm.rect().center() + QPoint(4, 0),
                pm.rect().center() + QPoint(-3, -6),
                pm.rect().center() + QPoint(-3, 6)
            ]
        painter.drawPolygon(*points)
        painter.end()
        return QIcon(pm)

    def prev_page(self):
        if self.page > 1:
            self.page -= 1
            self.refresh_main_content()

    def next_page(self):
        if self.page < self.total_pages:
            self.page += 1
            self.refresh_main_content()
