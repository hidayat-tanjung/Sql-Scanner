## 🛠 Detail Teknis & Struktur Kode
```console
📂 admin_finder/
 ├── 📜 admin_finder.py    # Script utama untuk scanning
 ├── 📜 requirements.txt   # Dependencies yang harus diinstal
 ├── 📜 README.md          # Dokumentasi proyek
 ├── 📂 logs/              # Folder untuk menyimpan hasil scanning
```
## Modul yang Digunakan
```console
✅ requests – Mengirim HTTP request untuk scanning
✅ threading – Menjalankan beberapa proses secara bersamaan
✅ pyfiglet – Membuat tampilan teks bergaya ASCII
✅ tabulate – Menampilkan hasil dalam bentuk tabel
✅ tqdm – Progress bar saat scanning
✅ colorama – Memberikan warna pada output terminal
```
## 🛠 Instalasi
```console
git clone https://github.com/hidayat-tanjung/Sql-Scanner.git
cd Sql-Scanner
pip install -r requirements.txt
python3 admin_finder.py
```
## 🚀 Cara Menggunakan
```console
python3 admin_finder.py
[?] Masukkan URL target (contoh: http://example.com): http://target.com
```
## 🚀 Mode MySQL Audit
Jika ingin melakukan audit keamanan MySQL, masukkan IP atau domain server:
```console
[?] Masukkan host MySQL (contoh: 127.0.0.1): 192.168.1.1
[?] Masukkan username MySQL (contoh: root): root
[?] Masukkan password MySQL: ****
```
## 👨‍💻 Kontribusi  

💬 Butuh bantuan atau ingin berkontribusi?  

- 🔍 **Laporkan bug atau minta fitur baru:** [Buka Issue](https://github.com/hidayat-tanjung/Sql-Scanner/issues)  
- 🚀 **Ingin berkontribusi? Buat Pull Request:** [Kirim Pull Request](https://github.com/hidayat-tanjung/Sql-Scanner/your-repo-name/pulls)

## ⚠ Disclaimer & Legalitas
Tool ini dibuat hanya untuk pengujian keamanan pribadi dan pentesting yang diizinkan.
🚨 Jangan digunakan untuk aktivitas ilegal atau tanpa izin dari pemilik sistem! 🚨

## 🛠 Cara Berkontribusi

Fork repository ini
1. Fork repository ini
2. Buat branch baru:
```console
git checkout -b fitur-baru
```
3. Lakukan perubahan & commit:
```console
git commit -m "Menambahkan fitur X"
```
4. Push ke GitHub:
```console
git push origin fitur-baru
```
5. Buat Pull Request! 🚀

## 📜 Contoh Output
```console
🔥 Welcome to Admin Panel & Sensitive File Scanner 🔥
By: [X3NUX] | Version: 1.0

[🔄] Initializing scanner...... DONE!

[🔎] Scanning admin panel untuk http://example.com...
✅ http://example.com/admin - Ditemukan (200 OK) - CVE-2021-29447

[🛑] Scanning file sensitif...
⚠️ http://example.com/.env - Ditemukan (200 OK)
❌ http://example.com/wp-config.php - Tidak ditemukan (404)

[🔍] MySQL Security Audit...
❌ Root login tidak diizinkan dari luar
⚠️ Database dapat diakses secara publik!

✔ Hasil scan disimpan di: admin_results.txt & sensitive_results.txt
```

## ⚠ Disclaimer & Legalitas
Tool ini dibuat hanya untuk pengujian keamanan pribadi dan pentesting yang diizinkan.
🚨 Jangan digunakan untuk aktivitas ilegal atau tanpa izin dari pemilik sistem! 🚨

🔥 Selamat Menggunakan & Stay Ethical! 🔥 🚀

