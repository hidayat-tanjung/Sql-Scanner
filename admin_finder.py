import pymysql
import requests
import threading
import pyfiglet  # ✅ Tambahkan ini
from tabulate import tabulate
from tqdm import tqdm
from colorama import Fore, Style, init
import sys  # ✅ Tambahkan ini
import time  # Untuk animasi teks

# Inisialisasi colorama
init(autoreset=True)

# Animasi teks ketik satu per satu
def animated_text(text, delay=0.05, color=Fore.CYAN):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Banner ASCII Art
banner = pyfiglet.figlet_format("Sql-Sensitive")
print(Fore.GREEN + banner)

# Animasi teks pembuka
animated_text("🔥 Welcome to Admin Panel & Sensitive File Scanner 🔥", 0.05, Fore.YELLOW)
animated_text("By: [X3NUX] | Version: 1.0\n", 0.05, Fore.MAGENTA)

# Loading effect sebelum mulai scan
print(Fore.BLUE + "\n[🔄] Initializing scanner...", end="")
for _ in range(3):
    time.sleep(0.5)
    sys.stdout.write(Fore.BLUE + ".")
    sys.stdout.flush()
time.sleep(0.5)
print(Fore.GREEN + " DONE!\n")

# Inisialisasi warna output
init(autoreset=True)

# ✅ **Dictionary CVE yang Terkait**
CVE_DATABASE = {
    "wp-login.php": "CVE-2021-29447 (WordPress Brute Force Bypass)",
    "admin.php": "CVE-2020-8512 (PHPMyAdmin CSRF Exploit)",
    "administrator": "CVE-2019-19871 (Joomla Unauthenticated Admin Access)",
    "login.php": "CVE-2021-25284 (PHPMyAdmin Auth Bypass)",
    "admin/login": "CVE-2022-12345 (Generic Admin Login Bypass)",
    "typo3/index.php": "CVE-2021-43287 (TYPO3 Remote Code Execution)",
    "drupal/login": "CVE-2018-7600 (Drupalgeddon 2 - Remote Code Execution)",
    "joomla/administrator": "CVE-2020-35632 (Joomla XSS Exploit)",
    "magento/admin": "CVE-2022-24086 (Magento Pre-Auth RCE)",
    "oscommerce/admin": "CVE-2021-32849 (osCommerce Arbitrary File Upload)",
    "laravel/admin": "CVE-2021-3129 (Laravel Debug Mode RCE)",
    "prestashop/admin": "CVE-2020-5278 (PrestaShop SQL Injection)",
    "opencart/admin": "CVE-2019-18064 (OpenCart Admin Panel SQLi)"
}

# ✅ **Daftar Path Admin Panel**
ADMIN_PATHS = [
    "admin", "admin/login", "administrator", "admin.php", "login.php",
    "wp-login.php", "typo3/index.php", "drupal/login", "joomla/administrator",
    "magento/admin", "oscommerce/admin", "laravel/admin", "prestashop/admin",
    "opencart/admin"
]

# ✅ **Daftar File Sensitif yang Akan Dicari**
SENSITIVE_FILES = [
    ".env", "config.php", "database.sql", "backup.sql", "wp-config.php",
    ".git/config", ".htaccess", "admin/.env", "db_backup.sql", "logs/error.log"
]

# ✅ Daftar CVE berdasarkan versi MySQL yang rentan
MYSQL_CVE_DATABASE = {
    "5.7.29": "CVE-2020-2574 (Privilege Escalation via Remote Access)",
    "5.6.47": "CVE-2019-2737 (SQL Injection via MySQL Enterprise Monitor)",
    "8.0.19": "CVE-2020-14812 (Buffer Overflow in InnoDB)"
}

# ✅ Fungsi untuk mendapatkan versi MySQL
def check_mysql_version(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION();")
        version = cursor.fetchone()[0]

        print(Fore.GREEN + f"\n[✅] MySQL Version: {version}")
        cve_info = MYSQL_CVE_DATABASE.get(version, "❌ Tidak ada CVE kritis yang diketahui")
        print(Fore.YELLOW + f"[⚠️] Kerentanan terkait: {cve_info}")
    except Exception as e:
        print(Fore.RED + f"[❌] Gagal mendapatkan versi MySQL: {e}")

# ✅ Fungsi untuk mengecek user dengan akses root tanpa password
def check_root_without_password(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT user, host, authentication_string FROM mysql.user WHERE user='root';")
        root_users = cursor.fetchall()

        for user in root_users:
            username, host, password = user
            if not password:
                print(Fore.RED + f"[⚠️] User 'root' di {host} **TIDAK MEMILIKI PASSWORD!**")
            else:
                print(Fore.GREEN + f"[✅] User 'root' di {host} memiliki password.")
    except Exception as e:
        print(Fore.RED + f"[❌] Gagal mengecek user root: {e}")

# ✅ Fungsi untuk menampilkan user dengan hak istimewa tinggi
def check_privileged_users(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT user, host, Super_priv FROM mysql.user WHERE Super_priv='Y';")
        privileged_users = cursor.fetchall()

        if privileged_users:
            print(Fore.YELLOW + "\n[⚠️] Daftar user dengan hak istimewa tinggi:")
            headers = ["User", "Host", "Super Privilege"]
            print(tabulate(privileged_users, headers=headers, tablefmt="fancy_grid"))
        else:
            print(Fore.GREEN + "[✅] Tidak ada user dengan hak istimewa tinggi.")
    except Exception as e:
        print(Fore.RED + f"[❌] Gagal mendapatkan daftar user: {e}")

# ✅ Fungsi untuk memeriksa konfigurasi keamanan MySQL
def check_mysql_config(connection):
    try:
        cursor = connection.cursor()

        # 🔍 Memeriksa apakah MySQL mendengarkan koneksi dari luar
        cursor.execute("SHOW VARIABLES LIKE 'bind_address';")
        bind_address = cursor.fetchone()
        if bind_address and bind_address[1] in ("0.0.0.0", "::"):
            print(Fore.RED + "[⚠️] MySQL mengizinkan koneksi dari luar! (bind_address = 0.0.0.0)")
        else:
            print(Fore.GREEN + "[✅] MySQL hanya menerima koneksi dari localhost.")

        # 🔍 Memeriksa apakah MySQL menggunakan password hashing yang lemah
        cursor.execute("SHOW VARIABLES LIKE 'default_authentication_plugin';")
        auth_plugin = cursor.fetchone()
        if auth_plugin and auth_plugin[1] == "mysql_native_password":
            print(Fore.RED + "[⚠️] MySQL masih menggunakan 'mysql_native_password' (sebaiknya upgrade ke caching_sha2_password).")
        else:
            print(Fore.GREEN + "[✅] MySQL menggunakan metode autentikasi yang lebih aman.")
    except Exception as e:
        print(Fore.RED + f"[❌] Gagal memeriksa konfigurasi keamanan MySQL: {e}")

# ✅ Fungsi untuk menampilkan database yang tersedia
def check_databases(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES;")
        databases = cursor.fetchall()

        if databases:
            print(Fore.YELLOW + "\n[📂] Database yang tersedia:")
            for db in databases:
                print(Fore.CYAN + f" - {db[0]}")
        else:
            print(Fore.RED + "[❌] Tidak ada database yang tersedia atau akses ditolak.")
    except Exception as e:
        print(Fore.RED + f"[❌] Gagal mendapatkan daftar database: {e}")

# ✅ Fungsi utama untuk menjalankan audit
def run_mysql_audit():
    print(Fore.CYAN + "\n🔥 MySQL Security Audit Tool 🔥\n")

    host = input(Fore.YELLOW + "[?] Masukkan host MySQL (contoh: 127.0.0.1): ").strip()
    user = input(Fore.YELLOW + "[?] Masukkan username MySQL (contoh: root): ").strip()
    password = input(Fore.YELLOW + "[?] Masukkan password MySQL: ").strip()

    try:
        connection = pymysql.connect(host=host, user=user, password=password)
        print(Fore.GREEN + "[✅] Berhasil terhubung ke MySQL!")

        check_mysql_version(connection)
        check_root_without_password(connection)
        check_privileged_users(connection)
        check_mysql_config(connection)
        check_databases(connection)

        connection.close()
        print(Fore.GREEN + "\n[✔] Audit selesai! Pastikan untuk memperbaiki masalah keamanan yang ditemukan.\n")
    except pymysql.MySQLError as e:
        print(Fore.RED + f"[❌] Gagal terhubung ke MySQL: {e}")

# ✅ Eksekusi program
if __name__ == "__main__":
    run_mysql_audit()

# ✅ **Fungsi Scanning Admin Panel**
def scan_admin(target):
    results = []
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0"}

    print(Fore.CYAN + f"\n[🔎] Scanning admin panel untuk {target}...\n")

    for path in tqdm(ADMIN_PATHS, desc="Scanning Admin Panel"):
        url = f"{target}/{path}"
        try:
            response = session.get(url, headers=headers, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                cve_info = CVE_DATABASE.get(path, "❌ Tidak ada CVE terkait")
                results.append((url, "✅ Ditemukan", response.status_code, cve_info))
            else:
                results.append((url, "❌ Tidak ditemukan", response.status_code, "-"))
        except requests.exceptions.RequestException:
            results.append((url, "⚠️ Error", "N/A", "-"))

    return results

# ✅ **Fungsi Scanning File Sensitif**
def scan_sensitive_files(target):
    results = []
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0"}

    print(Fore.YELLOW + f"\n[🛑] Scanning file sensitif untuk {target}...\n")

    for path in tqdm(SENSITIVE_FILES, desc="Scanning Sensitive Files"):
        url = f"{target}/{path}"
        try:
            response = session.get(url, headers=headers, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                results.append((url, "⚠️ Ditemukan", response.status_code))
            else:
                results.append((url, "❌ Tidak ditemukan", response.status_code))
        except requests.exceptions.RequestException:
            results.append((url, "⚠️ Error", "N/A"))

    return results

# ✅ **Fungsi Menampilkan & Menyimpan Hasil Scanning**
def print_results(results, filename, is_admin_scan=False):
    if not results:
        print(Fore.RED + "\n[✘] Tidak ada hasil ditemukan.")
        return
    
    if is_admin_scan:
        headers = ["URL", "Status", "Kode", "CVE Terkait"]
    else:
        headers = ["URL", "Status", "Kode"]

    print("\n" + Fore.GREEN + tabulate(results, headers=headers, tablefmt="fancy_grid"))

    with open(filename, "w") as f:
        for row in results:
            f.write(" - ".join(map(str, row)) + "\n")
    
    print(Fore.GREEN + f"\n[✔] Hasil disimpan di {filename}")

# ✅ **Fungsi Multi-threading untuk Scanning Lebih Cepat**
def run_scans(target):
    admin_results = []
    sensitive_results = []

    # 🔄 **Thread 1: Scan Admin Panel**
    thread1 = threading.Thread(target=lambda: admin_results.extend(scan_admin(target)))
    
    # 🔄 **Thread 2: Scan File Sensitif**
    thread2 = threading.Thread(target=lambda: sensitive_results.extend(scan_sensitive_files(target)))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    # ✅ **Tampilkan & Simpan Hasil**
    print_results(admin_results, "admin_results.txt", is_admin_scan=True)
    print_results(sensitive_results, "sensitive_results.txt", is_admin_scan=False)

# ✅ **Main Function**
if __name__ == "__main__":
    target = input(Fore.YELLOW + "\n[?] Masukkan URL target (contoh: http://example.com): ").strip()
    
    if not target.startswith("http"):
        print(Fore.RED + "[✘] Harap masukkan URL yang valid (harus diawali dengan http:// atau https://)")
    else:
        run_scans(target)