from PyQt5.QtWidgets import QWidget, QStackedLayout
from ui.main_window import MainWindow
from ui.admin_login import AdminLogin
from ui.admin_dashboard import AdminDashboard

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FARSFEA App")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QStackedLayout()
        self.setLayout(self.layout)

        self.main_window = MainWindow(self.show_admin_login)
        # Update: AdminLogin membutuhkan dua callback
        self.admin_login = AdminLogin(self.show_main_window, self.show_admin_dashboard)

        self.layout.addWidget(self.main_window)
        self.layout.addWidget(self.admin_login)

        self.layout.setCurrentWidget(self.main_window)

    def show_admin_login(self):
        self.layout.setCurrentWidget(self.admin_login)

    def show_main_window(self):
        self.layout.setCurrentWidget(self.main_window)
    
    def show_admin_dashboard(self, username):
        self.admin_dashboard = AdminDashboard(
            username=username,
            logout_callback=self.show_main_window,  # fungsi untuk logout
            menu_callbacks={
                "tambah_data": self.tambah_data,
                "hapus_data": self.hapus_data,
                "tampilkan_data": self.tampilkan_data,
                "laporan_absensi": self.laporan_absensi,
            }
        )
        self.layout.addWidget(self.admin_dashboard)
        self.layout.setCurrentWidget(self.admin_dashboard)

    # Stub menu functions, nanti bisa diimplementasikan
    def tambah_data(self):
        print("Tambah data karyawan ditekan")

    def hapus_data(self):
        print("Hapus data karyawan ditekan")

    def tampilkan_data(self):
        print("Tampilkan data karyawan ditekan")

    def laporan_absensi(self):
        print("Laporan absensi ditekan")
