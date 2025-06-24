import sqlite3
import hashlib
import os
import datetime
import pytz

DB_NAME = "data/app_data.db"

def get_db_connection():
    # Buat folder jika belum ada
    folder = os.path.dirname(DB_NAME)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ADMIN
def create_admin_table():
    conn = get_db_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
        """)
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_admin_user(username, password):
    conn = get_db_connection()
    try:
        with conn:
            conn.execute(
                "INSERT INTO admin_users (username, password_hash) VALUES (?, ?)",
                (username, hash_password(password))
            )
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_login(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT password_hash FROM admin_users WHERE username=?",
        (username,)
    )
    row = cur.fetchone()
    conn.close()
    if row and row["password_hash"] == hash_password(password):
        return True
    return False

# KARYAWAN
def create_karyawan_table():
    conn = get_db_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS karyawan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nik TEXT UNIQUE NOT NULL,
                nama TEXT NOT NULL
            );
        """)
    conn.close()

def tambah_karyawan(nik, nama):
    conn = get_db_connection()
    try:
        with conn:
            conn.execute(
                "INSERT INTO karyawan (nik, nama) VALUES (?, ?)",
                (nik, nama)
            )
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

def get_karyawan_by_nama(nama):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM karyawan WHERE nama = ?", (nama,))
    row = cur.fetchone()
    conn.close()
    return row

def get_all_karyawan():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM karyawan")
    rows = cur.fetchall()
    conn.close()
    return rows

# ABSENSI
def create_absensi_table():
    conn = get_db_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS absensi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nik TEXT NOT NULL,
                nama TEXT NOT NULL,
                waktu DATETIME DEFAULT CURRENT_TIMESTAMP,
                akurasi REAL
            );
        """)
    conn.close()

def tambah_absensi(nik, nama, akurasi):
    tz = pytz.timezone("Asia/Jakarta")
    waktu = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO absensi (nik, nama, waktu, akurasi) VALUES (?, ?, ?, ?)",
        (nik, nama, waktu, akurasi)
    )
    conn.commit()
    conn.close()

def get_laporan_absensi():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM absensi ORDER BY waktu DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

# --- Only needed for initial setup ---
if __name__ == "__main__":
    create_admin_table()
    create_karyawan_table()
    create_absensi_table()
    # Tambah admin user untuk pertama kali (boleh dihapus nanti)
    if add_admin_user("anita", "123"):
        print("Admin user berhasil dibuat!")
    else:
        print("Username sudah terdaftar!")

    # Tambah data karyawan (NIK urut: KRY001, KRY002, dst)
    daftar_nama = [
        "Aditya Satria Perdana",
        "Ainul Hali Ahmad",
        "Aisyah Kirana Putri Isyanto",
        "Andrian Andi Prakasa",
        "Anita Rossangelica",
        "Anton Joko Istiawan",
        "Bagus Widianto",
        "Bintang Pramudana Widi",
        "Bramasta Triananda Putra",
        "Devita Ayu Ramadhani",
        "Dwi Kartika Sari",
        "Enggal Nur Febrian Naufaldhianto",
        "Faisal Surya Nugraha",
        "Hafsa Chandra Rahmadiyanti",
        "Hasna Dzakiyyah Al Khansa",
        "Irene Evania Avelina",
        "Irvan Wahyu Arivianto",
        "Khumairoul Izzah",
        "M. Akbar Hidayatullah",
        "Malik Fizar Maulana",
        "Mastiyah",
        "Maula Izziddin Al Fatih",
        "Nabila Abidah Ardelia",
        "Narendra Briantara Putra",
        "Qothrun Nadaa",
        "Radika Septi Pradani",
        "Risma Sadhina",
        "Ruly Aryanti"
    ]

    for idx, nama in enumerate(daftar_nama, start=1):
        nik = f"KRY{idx:03d}"
        tambah_karyawan(nik, nama)

    print("Data karyawan berhasil diinput!")
