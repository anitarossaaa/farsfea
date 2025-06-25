from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QFrame,
    QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, QDateTime, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage
from data.database import tambah_absensi, get_karyawan_by_nama
import os

# ====== Ganti di sini kalau ingin ganti model atau label ======
MODEL_PATH = "farsfea100_cnn_fromtuning.keras"
LABELS_PATH = "labels.txt"
# =============================================================

class MainWindow(QWidget):
    def __init__(self, login_callback):
        super().__init__()
        self.login_callback = login_callback
        self.selected_file = None
        self.realtime_thread = None

        # Load model dan label map hanya sekali saat inisialisasi
        from tensorflow.keras.models import load_model
        from realtime_face import load_label_map
        self.model = load_model(MODEL_PATH)
        self.label_map = load_label_map(LABELS_PATH)

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

        # --- Kamera real-time ---
        self.camera_label = QLabel("Memuat kamera...")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setFixedSize(600, 300)
        self.camera_label.setStyleSheet("border: 1px solid #222; background: #fafafa;")
        center_layout.addWidget(self.camera_label, alignment=Qt.AlignCenter)

        # Label waktu dinamis
        self.datetime_label = QLabel()
        self.datetime_label.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(self.datetime_label)
        self.update_datetime_label()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime_label)
        self.timer.start(1000)

        # File input & test baris
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

        center_layout.addSpacing(10)

        # Preview hasil deteksi file (bukan kamera)
        preview_row = QHBoxLayout()
        preview_row.setAlignment(Qt.AlignHCenter)
        self.result_img_label = QLabel()
        self.result_img_label.setAlignment(Qt.AlignCenter)
        self.result_img_label.setFixedSize(280, 280)
        self.result_img_label.setStyleSheet("border: 1px solid #ddd; background: #fafafa; margin-bottom: 4px;")
        self.result_img_label.setText("Preview hasil deteksi di sini")
        preview_row.addWidget(self.result_img_label)
        center_layout.addLayout(preview_row)

        center_layout.addSpacing(20)
        main_layout.addLayout(center_layout)
        self.setLayout(main_layout)

        # --- Start kamera real-time thread (setelah layout) ---
        QTimer.singleShot(300, self.start_realtime_detection)  # delay supaya label sudah siap

    def update_datetime_label(self):
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
            self.file_label.setText(os.path.basename(file_name))
            self.show_result_image(file_name)
            QMessageBox.information(self, "Berhasil", "File gambar berhasil dipilih!")
        else:
            self.selected_file = None
            self.file_label.setText("Belum ada file dipilih")
            self.result_img_label.clear()
            self.result_img_label.setText("Preview hasil deteksi di sini")
            QMessageBox.warning(self, "Gagal", "File gambar tidak dipilih!")

    def show_result_image(self, file_path):
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            scaled = pixmap.scaled(self.result_img_label.width(), self.result_img_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.result_img_label.setPixmap(scaled)
        else:
            self.result_img_label.setText("Gagal load gambar.")

    def start_realtime_detection(self):
        try:
            from realtime_face import FaceRecognitionThread
            model_path = MODEL_PATH
            label_map = self.label_map
            self.realtime_thread = FaceRecognitionThread(model_path, label_map)
            self.realtime_thread.frame_updated.connect(self.update_camera_frame)
            self.realtime_thread.start()
        except Exception as e:
            self.camera_label.setText(f"Error: {e}")

    @pyqtSlot(QImage, list)
    def update_camera_frame(self, qimg, face_infos):
        # Tampilkan frame kamera
        self.camera_label.setPixmap(QPixmap.fromImage(qimg))
        # Absensi otomatis: Jika wajah tampil >=1 detik dan akurasi >=0.6, masukkan absensi (sekali)
        for face in face_infos:
            if face['detik'] >= 1.0 and face['akurat'] >= 0.6:
                # Ambil NIK dari nama
                row = get_karyawan_by_nama(face['nama'])
                if row:
                    nik = row['nik']
                    # Untuk mencegah duplikasi absensi dalam 1 sesi, bisa tambahkan memori (set/flag) jika ingin
                    tambah_absensi(nik, face['nama'], face['akurat'])
                    # (Bisa kasih notifikasi sekali, jika ingin)

    def test_absen_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Gagal", "Silakan pilih file gambar terlebih dahulu!")
            return

        try:
            import cv2, numpy as np
            model = self.model
            label_map = self.label_map
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            img = cv2.imread(self.selected_file)
            faces = face_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60))
            hasil = []
            img_out = img.copy()
            for i, (x, y, w, h) in enumerate(faces[:4]):
                face_img = img[y:y+h, x:x+w]
                face_resized = cv2.resize(face_img, (96, 96))
                face_array = face_resized.astype("float32") / 255.0
                face_array = np.expand_dims(face_array, axis=0)
                pred = model.predict(face_array)[0]
                pred_idx = np.argmax(pred)
                pred_acc = float(pred[pred_idx])
                nama = label_map.get(pred_idx, f"ID {pred_idx}")

                if pred_acc >= 0.6:
                    row = get_karyawan_by_nama(nama)
                    if row:
                        nik = row['nik']
                        tambah_absensi(nik, nama, pred_acc)
                    hasil.append(f"{nama} ({pred_acc:.2f})")
                    # Gambar bounding box dan label
                    cv2.rectangle(img_out, (x, y), (x+w, y+h), (0,255,0), 2)
                    cv2.putText(img_out, f"{nama} | {pred_acc:.2f}", (x, y+h+24),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

            # Tampilkan hasil ke preview
            img_rgb = cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB)
            h, w, ch = img_rgb.shape
            bytes_per_line = ch * w
            qimg = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            scaled = pixmap.scaled(self.result_img_label.width(), self.result_img_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.result_img_label.setPixmap(scaled)

            if hasil:
                QMessageBox.information(self, "Tes Absensi", f"Terdeteksi: {', '.join(hasil)}")
            else:
                QMessageBox.warning(self, "Tes Absensi", "Tidak ada wajah karyawan terdeteksi dengan akurasi tinggi.")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Terjadi error: {e}")

    def closeEvent(self, event):
        if self.realtime_thread:
            self.realtime_thread.stop()
            self.realtime_thread.wait()
        event.accept()
