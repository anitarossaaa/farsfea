import sqlite3

DB_NAME = "app_data.db"  # atau "data/app_data.db" jika path diubah

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Lihat semua tabel
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tabel yang ada di DB:")
for table in tables:
    print("-", table[0])

# Lihat isi tabel admin_users jika ada
if any(table[0] == 'admin_users' for table in tables):
    cursor.execute("SELECT * FROM admin_users;")
    rows = cursor.fetchall()
    print("\nIsi tabel admin_users:")
    for row in rows:
        print(row)
else:
    print("\ntabel admin_users tidak ditemukan.")

conn.close()
