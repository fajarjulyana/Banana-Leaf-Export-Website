
# Platform E-Commerce Ekspor Pertanian

Platform e-commerce dwibahasa (Indonesia/Inggris) yang dibangun dengan Flask untuk menjual produk pertanian premium, khusus dirancang untuk ekspor daun pisang internasional dan komoditas pertanian lainnya.

## Fitur Utama

### Fitur Pelanggan
- **Dukungan Dwibahasa**: Deteksi bahasa otomatis dengan pergantian manual antara Bahasa Indonesia dan Inggris
- **Multi-Mata Uang**: Dukungan USD dan IDR dengan konversi mata uang otomatis berdasarkan lokasi pengguna
- **Katalog Produk**: Jelajahi produk berdasarkan kategori dengan fungsi pencarian
- **Keranjang Belanja**: Tambah, update, dan hapus produk dengan manajemen kuantitas
- **Proses Checkout**: Registrasi pelanggan sederhana dan pemesanan
- **Desain Responsif**: Interface mobile-friendly menggunakan Bootstrap 5
- **Deteksi Negara**: Otomatis mendeteksi negara untuk menyesuaikan pengiriman dan mata uang
- **Info Pengiriman Dinamis**: Informasi pengiriman berbeda untuk dalam negeri dan internasional

### Fitur Admin
- **Dashboard**: Ringkasan pesanan, produk, dan statistik pendapatan
- **Manajemen Produk**: Tambah, edit, hapus, dan kelola inventori produk
- **Manajemen Pesanan**: Lihat, update status pesanan, dan kelola pesanan pelanggan
- **Pelacakan Pengiriman**: Lacak pengiriman dengan berbagai kurir (JNE, TIKI, DHL, FedEx, dll.)
- **Pengaturan Perusahaan**: Kelola informasi perusahaan dan kontak
- **Konten Multi-bahasa**: Kelola konten dalam Bahasa Indonesia dan Inggris
- **Manajemen Kategori**: Kelola kategori produk dengan nama dwibahasa
- **Upload Gambar**: Upload dan kelola gambar produk

## Stack Teknologi

### Backend
- **Flask**: Framework web Python
- **SQLAlchemy**: Database ORM dengan integrasi Flask-SQLAlchemy
- **Flask-Login**: Autentikasi pengguna dan manajemen sesi
- **Werkzeug**: Password hashing dan utilitas keamanan
- **SQLite/PostgreSQL**: Database (SQLite default, dapat dikonfigurasi ke PostgreSQL)

### Frontend
- **Bootstrap 5**: Framework CSS responsif
- **Font Awesome 6**: Library icon
- **Jinja2**: Template engine dengan dukungan dwibahasa
- **Vanilla JavaScript**: Interaktivitas client-side

## Instalasi & Setup

### Prasyarat
- Python 3.11+
- Git

### Quick Start di Replit
1. Fork repository ini di Replit
2. Aplikasi akan menginstall dependencies secara otomatis
3. Klik tombol "Run" untuk menjalankan server
4. Akses aplikasi di URL yang disediakan

### Development Lokal
```bash
# Clone repository
git clone <repository-url>
cd banana-export-website

# Install dependencies
pip install -r requirements.txt

# Inisialisasi database
python init_new_db.py

# Jalankan aplikasi
python main.py
```

## Konfigurasi

### Environment Variables
- `DATABASE_URL`: String koneksi database (default: SQLite)
- `SESSION_SECRET`: Secret key untuk manajemen sesi

### Kredensial Admin Default
- **Username**: `admin`
- **Password**: `admin123`

## Schema Database

### Model Utama
- **Admin**: Akun pengguna administratif
- **Category**: Kategori produk dengan nama dwibahasa
- **Product**: Produk dengan harga multi-mata uang dan deskripsi dwibahasa
- **Order**: Pesanan pelanggan dengan pelacakan pengiriman
- **OrderItem**: Item individual dalam pesanan
- **CompanySettings**: Informasi perusahaan yang dapat dikonfigurasi

### Fitur Utama Database
- Penyimpanan konten dwibahasa (Indonesia/Inggris)
- Dukungan multi-mata uang (USD/IDR)
- Pelacakan pengiriman komprehensif
- Manajemen timestamp otomatis

## API Endpoints

### Rute Pelanggan
- `GET /` - Homepage dengan produk unggulan
- `GET /products` - Katalog produk dengan filter
- `GET /product/<id>` - Halaman detail produk
- `POST /add_to_cart` - Tambah produk ke keranjang
- `GET /cart` - Manajemen keranjang belanja
- `GET /checkout` - Proses checkout
- `POST /place_order` - Submit pesanan
- `GET /set_language/<lang>` - Ubah bahasa

### Rute Admin
- `GET /admin` - Dashboard admin
- `GET /admin/login` - Login admin
- `GET /admin/products` - Manajemen produk
- `GET /admin/orders` - Manajemen pesanan
- `GET /admin/shipping` - Pelacakan pengiriman
- `GET /admin/settings` - Pengaturan perusahaan
- `GET /admin/categories` - Manajemen kategori

## Integrasi Pengiriman

### Kurir yang Didukung
- **Domestik (Indonesia)**: JNE, TIKI, POS Indonesia, SiCepat, J&T Express
- **Internasional**: DHL, FedEx, UPS

### Fitur Pelacakan
- Update status real-time
- Estimasi tanggal pengiriman
- Kalkulasi biaya pengiriman
- Penanganan domestik vs internasional

## Internasionalisasi

### Dukungan Bahasa
- **Bahasa Indonesia**: Default untuk pelanggan Indonesia
- **Bahasa Inggris**: Default untuk pelanggan internasional

### Fitur Auto-Detection
- Preferensi bahasa browser
- Analisis User-Agent
- Deteksi IP geografis
- Pergantian bahasa manual

## Kategori Produk

### Produk Utama
- **Daun Pisang** (Banana Leaves) - Premium export quality
- **Cocofit** - Coconut fiber products
- **Arang** (Charcoal) - Premium coconut shell charcoal
- **Sekam Padi** (Rice Husk) - Agricultural waste product

## Deployment di Replit

### Fitur Otomatis
- Deteksi dan setup environment
- Inisialisasi database
- Serving file statis
- Port forwarding (5000 → 80/443)

### Pertimbangan Produksi
- Middleware ProxyFix untuk kompatibilitas reverse proxy
- Keamanan sesi dengan secrets berbasis environment
- Connection pooling database
- Error logging dan monitoring

## Struktur File

```
├── admin_routes.py      # Rute dan logika panel admin
├── app.py              # Konfigurasi aplikasi Flask
├── main.py             # Entry point aplikasi
├── models.py           # Model database dan schema
├── routes.py           # Rute customer-facing
├── init_new_db.py      # Script inisialisasi database
├── static/
│   ├── css/style.css   # Stylesheet kustom
│   └── js/main.js      # Fungsionalitas JavaScript
└── templates/          # Template Jinja2
    ├── admin/          # Template panel admin
    ├── base.html       # Template dasar
    └── *.html          # Template halaman customer
```

## Fitur Keamanan

### Autentikasi
- Password hashing dengan Werkzeug
- Session management dengan Flask-Login
- CSRF protection pada form
- Secure admin panel

### Data Protection
- Validasi input form
- SQL injection protection via SQLAlchemy
- XSS protection via Jinja2 auto-escaping

## Troubleshooting

### Error Database
Jika mengalami error database:
```bash
# Jalankan workflow Initialize Database
python init_new_db.py
```

### Error Template
Jika template error, pastikan semua template menggunakan syntax Jinja2 yang benar dan memiliki filter yang diperlukan.

## Contributing

### Guidelines Development
1. Ikuti best practices Flask
2. Pertahankan dukungan konten dwibahasa
3. Test kedua mode mata uang (USD/IDR)
4. Pastikan mobile responsiveness
5. Pertahankan pemisahan admin/customer

### Menambah Fitur Baru
1. Update model database jika diperlukan
2. Tambah route ke blueprint yang sesuai
3. Buat template dwibahasa
4. Test dengan kombinasi bahasa/mata uang berbeda
5. Update panel admin jika applicable

## Lisensi

Project ini adalah software proprietary untuk bisnis ekspor pertanian.

## Support

Untuk dukungan teknis atau pertanyaan bisnis:
- **Email**: Hubungi admin melalui aplikasi
- **WhatsApp**: Tersedia di pengaturan perusahaan
- **Telepon**: Tercantum di informasi kontak perusahaan

---

**Catatan**: Aplikasi ini dioptimalkan untuk deployment Replit dan bisnis ekspor pertanian yang fokus pada produk Indonesia untuk pasar internasional.
