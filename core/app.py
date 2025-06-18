from PyQt5.QtWidgets import QWidget, QStackedLayout
from ui.main_window import MainWindow
from ui.admin_login import AdminLogin
from ui.admin_dashboard import AdminDashboard
from ui.admin_tampilkan_data_karyawan import AdminTampilkanDataKaryawan
from ui.admin_laporan_absensi_karyawan import AdminLaporanAbsensiKaryawan



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
                "tampilkan_data": self.tampilkan_data,
                "laporan_absensi": self.laporan_absensi,
            }
        )
        self.layout.addWidget(self.admin_dashboard)
        self.layout.setCurrentWidget(self.admin_dashboard)
        
    def tampilkan_data(self):
        self.tampilkan_karyawan_page = AdminTampilkanDataKaryawan(
            username=self.logged_in_username,
            logout_callback=self.show_main_window,
            menu_callbacks={
                "tampilkan_data": self.tampilkan_data,
                "laporan_absensi": self.laporan_absensi,
            }
        )
        self.layout.addWidget(self.tampilkan_karyawan_page)
        self.layout.setCurrentWidget(self.tampilkan_karyawan_page)

    def laporan_absensi(self):
        self.laporan_absensi_page = AdminLaporanAbsensiKaryawan(
            username=self.logged_in_username,
            logout_callback=self.show_main_window,
            menu_callbacks={
                "tampilkan_data": self.tampilkan_data,
                "laporan_absensi": self.laporan_absensi,
            }
        )
        self.layout.addWidget(self.laporan_absensi_page)
        self.layout.setCurrentWidget(self.laporan_absensi_page)
