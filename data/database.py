import sqlite3
import hashlib

DB_NAME = "data/app_data.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

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
        return False  # Username already exists
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

# --- For initial setup/testing (Run once to create table and admin user) ---
if __name__ == "__main__":
    create_admin_table()
    # Tambah admin user, ganti username/password sesuai kebutuhan
    if add_admin_user("bram", "123"):
        print("Admin user berhasil dibuat!")
    else:
        print("Username sudah terdaftar!")
