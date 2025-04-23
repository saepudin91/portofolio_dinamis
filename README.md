# Portofolio Dinamis dengan Streamlit

Aplikasi portofolio interaktif yang dibangun menggunakan Python dan Streamlit. Aplikasi ini memungkinkan kamu untuk menampilkan informasi pribadi, keahlian, serta pengalaman secara dinamis, serta dapat diubah langsung dari aplikasi tanpa perlu edit file.

## Fitur Utama

- Mode Tampilan Publik: Menampilkan informasi nama, deskripsi, keahlian, dan pengalaman.
- Mode Admin: Mengedit data portofolio seperti:
  - Nama dan deskripsi
  - Keahlian (tambah, edit, hapus)
  - Pengalaman (tambah)
  - Upload foto profil
- Data disimpan otomatis ke file data.json.
- Tidak perlu backend/database tambahan.

## Instalasi Lokal

1. Clone repositori:
    bash
    git clone https://github.com/username/portofolio_dinamis.git
    cd portofolio_dinamis
    

2. Install dependencies:
    bash
    pip install -r requirements.txt
    

3. Jalankan aplikasi:
    bash
    streamlit run app.py
    

## Hosting ke Streamlit Cloud

1. Push project ini ke GitHub.
2. Buka [streamlit.io/cloud](https://streamlit.io/cloud) dan hubungkan ke repo GitHub kamu.
3. Pilih file app.py sebagai entry point.
4. Jalankan aplikasi langsung di web.

## Penggunaan

- *Mode Admin*: Akses dari sidebar, masukkan password admin123.
- *Mode Publik*: Untuk dilihat oleh pengunjung umum.
- Semua data tersimpan otomatis di data.json.

## Contoh Tampilan

![Contoh tampilan aplikasi](screenshot.png)

## Tentang

Aplikasi ini dikembangkan oleh [muhamad saepudin] untuk membangun portofolio pribadi yang fleksibel dan mudah digunakan.

---

Silakan ganti [muhamad saepudin] dan screenshot.png dengan nama kamu dan tangkapan layar aplikasi jika ingin menambahkan.

Perlu bantu push ke GitHub juga?
