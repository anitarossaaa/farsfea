from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit,
    QFileDialog, QFrame
)
from PyQt5.QtCore import Qt
from ui.navbar import Navbar

class AdminTambahKaryawan(QWidget):
    def __init__(self, username, logout_callback, menu_callbacks):
        super().__init__()
        self.username = username
        self.logout_callback = logout_callback
        self.menu_callbacks = menu_callbacks
        self.selected_files = []
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

        # Main content (Form)
        main_content = QFrame()
        main_content.setStyleSheet("background-color: white;")
        main_content_layout = QVBoxLayout(main_content)
        main_content_layout.setAlignment(Qt.AlignCenter)

        # Judul form
        title_label = QLabel("Tambah data karyawan")
        title_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        main_content_layout.addWidget(title_label)
        main_content_layout.addSpacing(20)

        # Input: Nama
        nama_label = QLabel("NAMA")
        nama_label.setStyleSheet("font-size: 12px; font-weight: bold; letter-spacing: 2px;")
        self.nama_input = QLineEdit()
        self.nama_input.setPlaceholderText("Masukkan nama karyawan")
        self.nama_input.setFixedWidth(250)
        main_content_layout.addWidget(nama_label, alignment=Qt.AlignCenter)
        main_content_layout.addWidget(self.nama_input, alignment=Qt.AlignCenter)
        main_content_layout.addSpacing(10)

        # Input: NIK
        nik_label = QLabel("NIK")
        nik_label.setStyleSheet("font-size: 12px; font-weight: bold; letter-spacing: 2px;")
        self.nik_input = QLineEdit()
        self.nik_input.setPlaceholderText("Masukkan NIK")
        self.nik_input.setFixedWidth(250)
        self.nik_input.setMaxLength(20)
        self.nik_input.setValidator(None)  # Bisa diganti QIntValidator jika ingin membatasi hanya angka
        main_content_layout.addWidget(nik_label, alignment=Qt.AlignCenter)
        main_content_layout.addWidget(self.nik_input, alignment=Qt.AlignCenter)
        main_content_layout.addSpacing(10)

        # Input: Gambar
        gambar_label = QLabel("GAMBAR")
        gambar_label.setStyleSheet("font-size: 12px; font-weight: bold; letter-spacing: 2px;")
        self.gambar_btn = QPushButton("Choose a file")
        self.gambar_btn.setFixedWidth(250)
        self.gambar_btn.setStyleSheet("background-color: #e0e0e0; color: #444;")
        self.gambar_btn.clicked.connect(self.choose_file)
        main_content_layout.addWidget(gambar_label, alignment=Qt.AlignCenter)
        main_content_layout.addWidget(self.gambar_btn, alignment=Qt.AlignCenter)
        main_content_layout.addSpacing(18)

        # Tombol Tambahkan
        self.submit_btn = QPushButton("TAMBAHKAN")
        self.submit_btn.setFixedWidth(180)
        self.submit_btn.setStyleSheet("background-color: #4285f4; color: white; font-weight: bold; font-size: 16px; padding: 7px 0; border-radius: 4px;")
        self.submit_btn.clicked.connect(self.submit_form)
        main_content_layout.addWidget(self.submit_btn, alignment=Qt.AlignCenter)

        body_layout.addWidget(main_content)
        layout.addLayout(body_layout)
        self.setLayout(layout)

    def choose_file(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Pilih file gambar", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)"
        )
        if files:
            self.selected_files = files
            if len(files) == 1:
                self.gambar_btn.setText(files[0].split("/")[-1])
            else:
                self.gambar_btn.setText(f"{len(files)} files selected")
        else:
            self.gambar_btn.setText("Choose a file")

    def submit_form(self):
        # Ambil data dari form
        nama = self.nama_input.text()
        nik = self.nik_input.text()
        gambar_files = self.selected_files
        # Tambahkan validasi/aksi sesuai kebutuhan
        print("Nama:", nama)
        print("NIK:", nik)
        print("Files:", gambar_files)
        # TODO: Simpan data ke database, tampilkan notifikasi, dsb
