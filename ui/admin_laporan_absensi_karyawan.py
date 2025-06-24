from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QComboBox, QHeaderView
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor

from ui.navbar import Navbar
import datetime
import sqlite3

ROWS_PER_PAGE = 24

# --- KONFIGURASI JAM MASUK & KELUAR (dapat diedit kapan saja) ---
JAM_MASUK = 8      # Jam masuk (boleh integer/jam 24)
JAM_KELUAR = 16    # Jam keluar maksimal (boleh integer/jam 24)

def get_week_dates(week_num, month_num, year_num):
    """Mengembalikan list tuple (tanggal, bulan) untuk 7 hari pada minggu ke-X, dimulai Senin."""
    first_date = datetime.date(year_num, month_num, 1)
    first_monday = first_date + datetime.timedelta(days=(0 - first_date.weekday()) % 7)
    week_start = first_monday + datetime.timedelta(weeks=week_num - 1)
    dates = []
    for i in range(7):
        d = week_start + datetime.timedelta(days=i)
        dates.append((d.day, d.month))
    return dates

def get_week_of_month(date):
    first_day = date.replace(day=1)
    first_monday = first_day + datetime.timedelta(days=(0 - first_day.weekday()) % 7)
    week_num = ((date - first_monday).days // 7) + 1
    return max(week_num, 1)

def get_karyawan_list():
    db_path = "data/app_data.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT nama FROM karyawan ORDER BY nama")
    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows]

def get_absensi_for_karyawan(nama, year, month, tanggal):
    db_path = "data/app_data.db"
    tanggal_str = f"{year:04d}-{month:02d}-{tanggal:02d}"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT waktu FROM absensi
        WHERE nama=? AND DATE(waktu)=?
    """, (nama, tanggal_str))
    rows = cur.fetchall()
    conn.close()
    for r in rows:
        jam = int(r[0][11:13])
        if JAM_MASUK <= jam < JAM_KELUAR:
            return True
    return False

class AdminLaporanAbsensiKaryawan(QWidget):
    def __init__(self, username, logout_callback, menu_callbacks, page=1):
        super().__init__()
        self.username = username
        self.logout_callback = logout_callback
        self.menu_callbacks = menu_callbacks
        self.page = page

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
        self.month_combo.addItems(["Month"] + [
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ])
        self.year_combo = QComboBox()
        self.year_combo.addItems(["Year"] + [str(y) for y in range(2025, 2030)])

        # --- Set default ke hari ini ---
        today = datetime.date.today()
        default_year = today.year
        default_month = today.month
        default_week = get_week_of_month(today)
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
        self.refresh_main_content()

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

        # Ambil semua nama karyawan
        all_nama = get_karyawan_list()
        total_data = len(all_nama)
        self.total_pages = ((total_data - 1) // ROWS_PER_PAGE) + 1
        # Pagination
        start = (self.page - 1) * ROWS_PER_PAGE
        end = min(start + ROWS_PER_PAGE, total_data)
        page_nama = all_nama[start:end]

        # --- TABEL HEADER BERTINGKAT ---
        ROW_HEADER = 2  # dua baris untuk header
        COL_COUNT = 9

        table = QTableWidget(ROW_HEADER + len(page_nama), COL_COUNT)
        # Stretch semua kolom sesuai area yang tersedia
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.NoSelection)
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)

        # Header baris pertama (angka tanggal)
        table.setItem(0, 0, QTableWidgetItem("Nama"))
        for i in range(7):
            tgl, bln = tanggal_header[i]
            table.setItem(0, i + 1, QTableWidgetItem(str(tgl)))
        table.setItem(0, 8, QTableWidgetItem("Jumlah Kehadiran"))

        # Header baris kedua (SELALU hari Senin-Minggu, konstan)
        table.setItem(1, 0, QTableWidgetItem(""))  # merge nanti
        for i in range(7):
            table.setItem(1, i + 1, QTableWidgetItem(hari[i]))
        table.setItem(1, 8, QTableWidgetItem(""))  # merge nanti

        # Merge cell di header kolom pertama dan terakhir (Nama & Jumlah Kehadiran)
        table.setSpan(0, 0, 2, 1)      # "Nama" (baris 0 & 1, kolom 0)
        table.setSpan(0, 8, 2, 1)      # "Jumlah Kehadiran" (baris 0 & 1, kolom 8)

        # Isi data absensi karyawan
        today = datetime.date.today()
        for row_idx, nama in enumerate(page_nama):
            table.setItem(ROW_HEADER + row_idx, 0, QTableWidgetItem(nama))
            hadir_count = 0
            for j, (tgl, bln) in enumerate(tanggal_header):
                if not tgl:
                    table.setItem(ROW_HEADER + row_idx, j + 1, QTableWidgetItem(""))
                    continue
                cell_date = datetime.date(year, bln, tgl)
                is_today = (cell_date == today)
                is_future = (cell_date > today)
                hadir = get_absensi_for_karyawan(nama, year, bln, tgl)

                # Hari besok/seterusnya: cell kosong
                if is_future:
                    table.setItem(ROW_HEADER + row_idx, j + 1, QTableWidgetItem(""))
                # Hari ini: hanya tulis OK jika hadir, kosong jika belum absen
                elif is_today:
                    now = datetime.datetime.now()
                    jam_sekarang = now.hour
                    if hadir:
                        item = QTableWidgetItem("OK")
                        item.setBackground(QColor("#c8e6c9"))
                        table.setItem(ROW_HEADER + row_idx, j + 1, item)
                        hadir_count += 1
                    else:
                        # Tulis NOK hanya jika sudah lewat jam keluar maksimal
                        if jam_sekarang >= JAM_KELUAR:
                            table.setItem(ROW_HEADER + row_idx, j + 1, QTableWidgetItem("NOK"))
                        else:
                            table.setItem(ROW_HEADER + row_idx, j + 1, QTableWidgetItem(""))
                # Hari lalu: tulis OK atau NOK
                else:
                    if hadir:
                        item = QTableWidgetItem("OK")
                        item.setBackground(QColor("#c8e6c9"))  # hijau muda
                        table.setItem(ROW_HEADER + row_idx, j + 1, item)
                        hadir_count += 1
                    else:
                        table.setItem(ROW_HEADER + row_idx, j + 1, QTableWidgetItem("NOK"))
            table.setItem(ROW_HEADER + row_idx, 8, QTableWidgetItem(str(hadir_count)))

        # Pakai stretch agar memenuhi main_content
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

        pagination_layout.addWidget(page_info)
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
