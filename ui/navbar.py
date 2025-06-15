from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt

class Navbar(QWidget):
    def __init__(self, menu_callbacks):
        """
        menu_callbacks: dict, key nama menu, value fungsi callback
        """
        super().__init__()
        self.menu_callbacks = menu_callbacks
        self.init_ui()
    
    def init_ui(self):
        self.setFixedWidth(220)
        self.setStyleSheet("background-color: #c8e6c9;")  # warna hijau muda

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Header burger dan menu lainnya
        header_layout = QHBoxLayout()
        burger_btn = QPushButton("☰")
        burger_btn.setFixedSize(30, 30)
        burger_btn.setStyleSheet("background: none; border: none; font-size: 18px; margin-left: 5px;")
        menu_label = QLabel("Menu Lainnya")
        menu_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-left: 10px;")
        header_layout.addWidget(burger_btn)
        header_layout.addWidget(menu_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        layout.addSpacing(20)

        # Data Karyawan
        karyawan_title = QLabel("Data Karyawan")
        karyawan_title.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(karyawan_title)
        
        tambah_btn = QPushButton("• Tambah data")
        tambah_btn.setStyleSheet("text-align: left; background: none; border: none; font-size: 12px; margin-left: 15px;")
        tambah_btn.clicked.connect(lambda: self.menu_callbacks["tambah_data"]())
        layout.addWidget(tambah_btn)

        hapus_btn = QPushButton("• Hapus data")
        hapus_btn.setStyleSheet("text-align: left; background: none; border: none; font-size: 12px; margin-left: 15px;")
        hapus_btn.clicked.connect(lambda: self.menu_callbacks["hapus_data"]())
        layout.addWidget(hapus_btn)

        tampil_btn = QPushButton("• Tampilkan data")
        tampil_btn.setStyleSheet("text-align: left; background: none; border: none; font-size: 12px; margin-left: 15px;")
        tampil_btn.clicked.connect(lambda: self.menu_callbacks["tampilkan_data"]())
        layout.addWidget(tampil_btn)

        layout.addSpacing(15)
        
        # Absensi
        absensi_title = QLabel("Absensi")
        absensi_title.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(absensi_title)
        laporan_btn = QPushButton("• Laporan Absensi")
        laporan_btn.setStyleSheet("text-align: left; background: none; border: none; font-size: 12px; margin-left: 15px;")
        laporan_btn.clicked.connect(lambda: self.menu_callbacks["laporan_absensi"]())
        layout.addWidget(laporan_btn)

        layout.addStretch()
        self.setLayout(layout)
