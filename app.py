import streamlit as st
import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Portofolio", layout="centered")

# Load data dari file JSON
def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return {
        "profile": {}, 
        "skills": [], 
        "pengalaman": [], 
        "identitas": {}, 
        "projects": []
    }

# Simpan data ke file JSON
def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

# Simpan ke Google Sheets
def simpan_ke_google_sheet(nama, email, pesan):
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Data Portofolio").sheet1
    sheet.append_row([nama, email, pesan])

# Sidebar untuk memilih mode
st.sidebar.title("Mode")
mode = st.sidebar.radio("Pilih mode:", ["Tampilan Publik", "Edit (Admin)"])

data = load_data()

# Pastikan file foto profil selalu ada
if not os.path.exists("profile_photo.jpg"):
    with open("profile_photo.jpg", "wb") as f:
        pass

# Tampilan Publik
if mode == "Tampilan Publik":
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

        .custom-title {
            font-family: 'Poppins', sans-serif;
            font-size: 6vw;
            text-align: center;
            color: #2C3E50;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }

        @media (min-width: 768px) {
            .custom-title {
                font-size: 2rem;
            }
        }

        .custom-desc {
            font-family: 'Poppins', sans-serif;
            font-size: 3.8vw;
            text-align: center;
            color: #555;
            margin-bottom: 1.5rem;
            font-weight: 400;
        }

        @media (min-width: 768px) {
            .custom-desc {
                font-size: 1.2rem;
            }
        }

        .section-title {
            font-family: 'Poppins', sans-serif;
            font-size: 5vw;
            color: #34495E;
            margin-top: 2rem;
            font-weight: 600;
            border-bottom: 2px solid #ddd;
            padding-bottom: 0.2rem;
        }

        @media (min-width: 768px) {
            .section-title {
                font-size: 1.5rem;
            }
        }

        .skill-name {
            font-family: 'Poppins', sans-serif;
            font-size: 0.95rem;
            margin-bottom: 0.2rem;
            font-weight: 500;
        }

        .pengalaman-text, .project-desc {
            font-family: 'Poppins', sans-serif;
            font-size: 0.95rem;
            color: #444;
        }

        .hubungi {
            font-family: 'Poppins', sans-serif;
            font-size: 1rem;
            text-align: center;
            margin-top: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if os.path.getsize("profile_photo.jpg") > 0:
        st.image("profile_photo.jpg", caption="Foto Profil", use_container_width=True)
    else:
        st.write("Foto belum diunggah")

    st.markdown(f"<div class='custom-title'>{data['profile'].get('nama', 'Nama Belum Diisi')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='custom-desc'>{data['profile'].get('deskripsi', 'Deskripsi belum diisi')}</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>🛠 Keahlian</div>", unsafe_allow_html=True)
    for skill in data["skills"]:
        if ":" in skill:
            nama, nilai = skill.split(":")
            st.markdown(f"<div class='skill-name'>{nama.strip()} ({nilai.strip()}%)</div>", unsafe_allow_html=True)
            try:
                st.progress(int(nilai.strip()))
            except:
                st.write(f"(Format salah: {skill})")
        else:
            st.write(skill)

    st.markdown("<div class='section-title'>💼 Pengalaman</div>", unsafe_allow_html=True)
    for exp in data["pengalaman"]:
        st.markdown(f"<div class='pengalaman-text'><strong>{exp['judul']} ({exp['tahun']})</strong><br>{exp['deskripsi']}</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>📁 Portofolio Proyek</div>", unsafe_allow_html=True)
    for proj in data.get("projects", []):
        st.image(proj["gambar"], use_column_width=True)
        st.markdown(f"<div class='pengalaman-text'><strong>{proj['judul']} ({proj['tahun']})</strong></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='project-desc'>{proj['deskripsi']}</div>", unsafe_allow_html=True)
        if proj.get("link"):
            st.markdown(f"[Lihat Proyek]({proj['link']})", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>📞 Hubungi Saya</div>", unsafe_allow_html=True)
    st.markdown("<div class='hubungi'><a href='https://wa.me/6287810059643' target='_blank'>WhatsApp</a></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>💬 Kirim Pesan ke Admin</div>", unsafe_allow_html=True)
    with st.form("form_pesan"):
        nama_pengirim = st.text_input("Nama")
        email_pengirim = st.text_input("Email")
        isi_pesan = st.text_area("Pesan")
        submit = st.form_submit_button("Kirim")

        if submit and nama_pengirim and isi_pesan:
            try:
                simpan_ke_google_sheet(nama_pengirim, email_pengirim, isi_pesan)
                st.success("Pesan berhasil dikirim dan disimpan ke Google Sheets!")
            except Exception as e:
                st.error(f"Gagal menyimpan ke Google Sheets: {e}")

# Mode admin tetap sama seperti sebelumnya
elif mode == "Edit (Admin)":
    ... # Seluruh bagian Edit (Admin) tetap sama
