from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QComboBox
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon, QPixmap, QPainter

from ui.navbar import Navbar
import datetime

DUMMY_ABSEN = [
    {
        "nama": f"Nama {i+1}",
        "minggu": ["OK" if j == 0 and i == 0 else ("NOK" if j == 1 and i == 0 else "") for j in range(7)],
        "jumlah": 1 if i == 0 else 0
    }
    for i in range(35)
]
ROWS_PER_PAGE = 7

def get_week_dates(week_num, month_num, year_num):
    first_date = datetime.date(year_num, month_num, 1)
    first_monday = first_date + datetime.timedelta(days=(0 - first_date.weekday()) % 7)
    week_start = first_monday + datetime.timedelta(weeks=week_num - 1)
    dates = []
    for i in range(7):
        d = week_start + datetime.timedelta(days=i)
        if d.month == month_num:
            dates.append(d.day)
        else:
            dates.append("")
    return dates

def get_week_of_month(date):
    first_day = date.replace(day=1)
    first_monday = first_day + datetime.timedelta(days=(0 - first_day.weekday()) % 7)
    week_num = ((date - first_monday).days // 7) + 1
    return max(week_num, 1)

class AdminLaporanAbsensiKaryawan(QWidget):
    def __init__(self, username, logout_callback, menu_callbacks, page=1):
        super().__init__()
        self.username = username
        self.logout_callback = logout_callback
        self.menu_callbacks = menu_callbacks
        self.page = page
        self.total_pages = ((len(DUMMY_ABSEN) - 1) // ROWS_PER_PAGE) + 1

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

        # Main content area
        self.main_content = QFrame()
        self.main_content.setStyleSheet("background-color: white;")
        self.body_layout.addWidget(self.main_content)

        # --- Dropdown di luar refresh_main_content biar sinyal tidak double ---
        filter_layout = QHBoxLayout()
        self.week_combo = QComboBox()
        self.week_combo.addItems(["Week"] + [f"Week {i+1}" for i in range(5)])
        self.month_combo = QComboBox()
        self.month_combo.addItems(["Month"] + ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"])
        self.year_combo = QComboBox()
        self.year_combo.addItems(["Year"] + [str(y) for y in range(2025, 2030)])

        # --- Set default ke hari ini ---
        today = datetime.date.today()
        default_year = today.year
        default_month = today.month
        default_week = get_week_of_month(today)
        # Cek di list year, kalau belum ada (misal run 2024, list mulai 2025), fallback ke index 1 (2025)
        year_list = [int(self.year_combo.itemText(i)) for i in range(1, self.year_combo.count())]
        year_idx = year_list.index(default_year) + 1 if default_year in year_list else 1
        self.year_combo.setCurrentIndex(year_idx)
        self.month_combo.setCurrentIndex(default_month)
        self.week_combo.setCurrentIndex(default_week)

        filter_layout.addWidget(self.week_combo)
        filter_layout.addWidget(self.month_combo)
        filter_layout.addWidget(self.year_combo)
        filter_layout.addStretch()

        # Connect dropdown untuk trigger refresh
        self.week_combo.currentIndexChanged.connect(self.refresh_main_content)
        self.month_combo.currentIndexChanged.connect(self.refresh_main_content)
        self.year_combo.currentIndexChanged.connect(self.refresh_main_content)

        self.filter_layout = filter_layout
        self.refresh_main_content()  # Panggil isi awal

    def refresh_main_content(self):
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

        # --- Tambahkan filter layout (biar dropdown tetap) ---
        main_content_layout.addLayout(self.filter_layout)
        main_content_layout.addSpacing(10)

        # Judul tengah
        title_label = QLabel("LAPORAN ABSENSI")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 15px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_content_layout.addWidget(title_label)
        main_content_layout.addSpacing(10)

        # Ambil value week, month, year
        week_idx = self.week_combo.currentIndex()
        month_idx = self.month_combo.currentIndex()
        year_idx = self.year_combo.currentIndex()

        week = week_idx if week_idx > 0 else 1
        month = month_idx if month_idx > 0 else 1
        year = 2025 + (year_idx - 1) if year_idx > 0 else 2025

        tanggal_header = get_week_dates(week, month, year)
        hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

        # Data untuk halaman ini
        start = (self.page - 1) * ROWS_PER_PAGE
        end = min(start + ROWS_PER_PAGE, len(DUMMY_ABSEN))
        page_data = DUMMY_ABSEN[start:end]

        # --- TABEL HEADER BERTINGKAT ---
        ROW_HEADER = 2  # dua baris untuk header
        COL_COUNT = 9

        table = QTableWidget(ROW_HEADER + len(page_data), COL_COUNT)
        table.setFixedWidth(600)
        table.setColumnWidth(0, 180)   # Nama
        for i in range(1, 8):
            table.setColumnWidth(i, 80)  # Kolom tanggal
        table.setColumnWidth(8, 120)   # Jumlah Kehadiran
        table.setFixedHeight(280)
        
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.NoSelection)
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)

        # Header baris pertama (angka tanggal)
        table.setItem(0, 0, QTableWidgetItem("Nama"))
        for i in range(7):
            table.setItem(0, i + 1, QTableWidgetItem(str(tanggal_header[i]) if tanggal_header[i] else ""))
        table.setItem(0, 8, QTableWidgetItem("Jumlah Kehadiran"))

        # Header baris kedua (hari)
        table.setItem(1, 0, QTableWidgetItem(""))  # merge nanti
        for i in range(7):
            table.setItem(1, i + 1, QTableWidgetItem(hari[i]))
        table.setItem(1, 8, QTableWidgetItem(""))  # merge nanti

        # Merge cell di header kolom pertama dan terakhir (Nama & Jumlah Kehadiran)
        table.setSpan(0, 0, 2, 1)      # "Nama" (baris 0 & 1, kolom 0)
        table.setSpan(0, 8, 2, 1)      # "Jumlah Kehadiran" (baris 0 & 1, kolom 8)

        # Isi data
        for row_idx, row in enumerate(page_data):
            table.setItem(ROW_HEADER + row_idx, 0, QTableWidgetItem(row["nama"]))
            for j in range(7):
                table.setItem(ROW_HEADER + row_idx, j + 1, QTableWidgetItem(row["minggu"][j]))
            table.setItem(ROW_HEADER + row_idx, 8, QTableWidgetItem(str(row["jumlah"])))

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
