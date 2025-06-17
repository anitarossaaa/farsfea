from PyQt5.QtWidgets import QWidget, QStackedLayout
from ui.main_window import MainWindow
from ui.admin_login import AdminLogin
from ui.admin_dashboard import AdminDashboard
from ui.admin_tambah_karyawan import AdminTambahKaryawan
from ui.admin_hapus_karyawan import AdminHapusKaryawan


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FARSFEA App")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QStackedLayout()
        self.setLayout(self.layout)

        self.main_window = MainWindow(self.show_admin_login)
        self.admin_login = AdminLogin(self.show_main_window, self.show_admin_dashboard)

        self.layout.addWidget(self.main_window)
        self.layout.addWidget(self.admin_login)

        self.layout.setCurrentWidget(self.main_window)

        # Tambahkan variabel untuk simpan username login (opsional)
        self.logged_in_username = None

    def show_admin_login(self):
        self.layout.setCurrentWidget(self.admin_login)

    def show_main_window(self):
        self.layout.setCurrentWidget(self.main_window)
    
    def show_admin_dashboard(self, username):
        self.logged_in_username = username  # Simpan username yg login
        self.admin_dashboard = AdminDashboard(
            username=username,
            logout_callback=self.show_main_window,
            menu_callbacks={
                "tambah_data": self.tambah_data,
                "hapus_data": self.hapus_data,
                "tampilkan_data": self.tampilkan_data,
                "laporan_absensi": self.laporan_absensi,
            }
        )
        self.layout.addWidget(self.admin_dashboard)
        self.layout.setCurrentWidget(self.admin_dashboard)

    def tambah_data(self):
        # Tampilkan halaman tambah karyawan
        self.tambah_karyawan_page = AdminTambahKaryawan(
            username=self.logged_in_username,
            logout_callback=self.show_main_window,
            menu_callbacks={
                "tambah_data": self.tambah_data,
                "hapus_data": self.hapus_data,
                "tampilkan_data": self.tampilkan_data,
                "laporan_absensi": self.laporan_absensi,
            }
        )
        self.layout.addWidget(self.tambah_karyawan_page)
        self.layout.setCurrentWidget(self.tambah_karyawan_page)

    def hapus_data(self):
        # Tampilkan halaman hapus karyawan
        self.hapus_karyawan_page = AdminHapusKaryawan(
            username=self.logged_in_username,
            logout_callback=self.show_main_window,
            menu_callbacks={
                "tambah_data": self.tambah_data,
                "hapus_data": self.hapus_data,
                "tampilkan_data": self.tampilkan_data,
                "laporan_absensi": self.laporan_absensi,
            }
        )
        self.layout.addWidget(self.hapus_karyawan_page)
        self.layout.setCurrentWidget(self.hapus_karyawan_page)

    def tampilkan_data(self):
        print("Tampilkan data karyawan ditekan")
        # Buat halaman tampilkan data jika sudah ada

    def laporan_absensi(self):
        print("Laporan absensi ditekan")
        # Buat halaman laporan absensi jika sudah ada
