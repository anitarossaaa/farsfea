from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QFrame,
    QFileDialog, QMessageBox, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QPixmap

class MainWindow(QWidget):
    def __init__(self, login_callback):
        super().__init__()
        self.login_callback = login_callback
        self.selected_file = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # HEADER stretch penuh
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #2ecc71;")
        header_frame.setFixedHeight(50)
        header_hbox = QHBoxLayout(header_frame)
        header_hbox.setContentsMargins(15, 0, 15, 0)

        title = QLabel("FARSFEA")
        title.setStyleSheet("font-weight: bold; font-size: 18px; margin-left: 10px;")
        login_btn = QPushButton("ADMIN LOGIN")
        login_btn.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; padding: 5px 18px; border-radius: 6px;")
        login_btn.clicked.connect(self.login_callback)

        header_hbox.addWidget(title)
        header_hbox.addStretch()
        header_hbox.addWidget(login_btn)
        main_layout.addWidget(header_frame)

        # Konten utama
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        center_layout.setSpacing(14)

        # Title
        page_title = QLabel("Face Recognition System for Employee Attendance")
        page_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 15px;")
        page_title.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(page_title)

        # Placeholder kamera real time
        box = QFrame()
        box.setStyleSheet("background-color: #f0f0f0; border: 1px solid black;")
        box.setFixedSize(600, 300)
        center_layout.addWidget(box, alignment=Qt.AlignCenter)

        # Label waktu dinamis
        self.datetime_label = QLabel()
        self.datetime_label.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(self.datetime_label)
        self.update_datetime_label()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime_label)
        self.timer.start(1000)

        # Baris file input dan tombol
        file_row = QHBoxLayout()
        file_row.setAlignment(Qt.AlignCenter)
        self.file_label = QLabel("Belum ada file dipilih")
        self.file_label.setStyleSheet("background: #eee; border: 1px solid #ccc; padding: 3px 12px; border-radius: 4px;")
        file_row.addWidget(self.file_label)

        file_btn = QPushButton("Pilih File Gambar")
        file_btn.clicked.connect(self.open_file_dialog)
        file_row.addWidget(file_btn)

        test_btn = QPushButton("Tes Absensi dengan File Gambar")
        test_btn.setStyleSheet("background-color: #3498db; color: white; font-weight: bold;")
        test_btn.clicked.connect(self.test_absen_file)
        file_row.addWidget(test_btn)
        center_layout.addLayout(file_row)

        # Spacer kecil antara tombol dan hasil deteksi
        center_layout.addSpacing(10)

        # === Preview hasil deteksi center ===
        preview_row = QHBoxLayout()
        preview_row.setAlignment(Qt.AlignHCenter)
        self.result_img_label = QLabel()
        self.result_img_label.setAlignment(Qt.AlignCenter)
        self.result_img_label.setFixedSize(280, 280)
        self.result_img_label.setStyleSheet("border: 1px solid #ddd; background: #fafafa; margin-bottom: 4px;")
        self.result_img_label.setText("Preview hasil deteksi di sini")
        preview_row.addWidget(self.result_img_label)
        center_layout.addLayout(preview_row)

        # Tambahkan spacing kecil di bawah, bukan spacer expandable!
        center_layout.addSpacing(20)  # Space kecil saja agar tidak nempel bawah

        main_layout.addLayout(center_layout)
        # JANGAN tambahkan main_layout.addSpacerItem(QSpacerItem(..., QSizePolicy.Expanding)) di bawah

        self.setLayout(main_layout)


    def update_datetime_label(self):
        # Format ke string lokal, misal: "Senin, 10 Juni 2025 - 13:40:01"
        hari_id = [
            "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"
        ]
        bulan_id = [
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ]
        now = QDateTime.currentDateTime()
        day_of_week = now.date().dayOfWeek()  # 1=Senin, 7=Minggu
        day = now.date().day()
        month = now.date().month()
        year = now.date().year()
        jam = now.time().toString("HH:mm:ss")
        tanggal = f"{hari_id[day_of_week-1]}, {day} {bulan_id[month-1]} {year} - {jam}"
        self.datetime_label.setText(f"Real-time face detection ({tanggal})")

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Pilih File Gambar",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_name:
            self.selected_file = file_name
            self.file_label.setText(file_name.split("/")[-1])
            self.show_result_image(file_name)
            QMessageBox.information(self, "Berhasil", "File gambar berhasil dipilih!")
        else:
            self.selected_file = None
            self.file_label.setText("Belum ada file dipilih")
            self.result_img_label.clear()
            self.result_img_label.setText("Preview hasil deteksi di sini")
            QMessageBox.warning(self, "Gagal", "File gambar tidak dipilih!")

    def test_absen_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Gagal", "Silakan pilih file gambar terlebih dahulu!")
        else:
            QMessageBox.information(self, "Tes Absensi", f"Tes absensi dengan file '{self.selected_file.split('/')[-1]}' berhasil (dummy).")

    def show_result_image(self, file_path):
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            scaled = pixmap.scaled(self.result_img_label.width(), self.result_img_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.result_img_label.setPixmap(scaled)
        else:
            self.result_img_label.setText("Gagal load gambar.")
