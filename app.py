import streamlit as st
import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Portofolio", layout="centered")

# Load dan Simpan Data JSON
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

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

# Simpan Pesan ke Google Sheets
from oauth2client.service_account import ServiceAccountCredentials
import gspread

def simpan_ke_google_sheet(nama, email, pesan):
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        dict(st.secrets["gcp_service_account"]), scope
    )
    client = gspread.authorize(creds)

    try:
        sheet = client.open("Data Portofolio").worksheet("Pesan Pengunjung")
        sheet.append_row([nama, email, pesan])
    except Exception as e:
        st.error(f"Gagal menyimpan ke Google Sheets: {e}")
# Inisialisasi
data = load_data()
if not os.path.exists("profile_photo.jpg"):
    with open("profile_photo.jpg", "wb") as f:
        pass

# Sidebar Mode
st.sidebar.title("Mode")
mode = st.sidebar.radio("Pilih mode:", ["Tampilan Publik", "Edit (Admin)"])

# ==========================
# ========== MODE PUBLIK ==========
# ==========================
if mode == "Tampilan Publik":
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        .custom-title { font-family: 'Poppins', sans-serif; font-size: 6vw; text-align: center; color: #2C3E50; font-weight: 600; }
        .custom-desc { font-family: 'Poppins', sans-serif; font-size: 3.8vw; text-align: center; color: #555; font-weight: 400; }
        .section-title { font-family: 'Poppins', sans-serif; font-size: 5vw; color: #34495E; font-weight: 600; border-bottom: 2px solid #ddd; padding-bottom: 0.2rem; }
        .skill-name { font-family: 'Poppins', sans-serif; font-size: 0.95rem; font-weight: 500; }
        .pengalaman-text, .project-desc { font-family: 'Poppins', sans-serif; font-size: 0.95rem; color: #444; }
        .hubungi { font-family: 'Poppins', sans-serif; font-size: 1rem; text-align: center; margin-top: 2rem; }
        </style>
    """, unsafe_allow_html=True)

    if os.path.getsize("profile_photo.jpg") > 0:
        st.image("profile_photo.jpg", caption="Foto Profil", use_container_width=True)
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

# ==========================
# ========== MODE ADMIN ==========
# ==========================
elif mode == "Edit (Admin)":
    st.title("Mode Edit Portofolio")
    password = st.text_input("Masukkan Password Admin", type="password")
    if password != "admin123":
        st.warning("Masukkan password untuk mengakses mode edit.")
        st.stop()

    with st.expander("Profil dan Identitas", expanded=True):
        nama = st.text_input("Nama", value=data["profile"].get("nama", ""))
        deskripsi = st.text_area("Deskripsi", value=data["profile"].get("deskripsi", ""))
        alamat = st.text_input("Alamat", value=data["profile"].get("alamat", ""))
        jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"], 
                                     index=0 if data["profile"].get("jenis_kelamin") == "Laki-laki" else 1)
        agama = st.text_input("Agama", value=data["profile"].get("agama", ""))
        tanggal_lahir = st.date_input("Tanggal Lahir")
        instagram = st.text_input("Instagram", value=data["profile"].get("instagram", ""))
        linkedin = st.text_input("LinkedIn", value=data["profile"].get("linkedin", ""))
        github = st.text_input("GitHub", value=data["profile"].get("github", ""))

    with st.expander("Foto Profil"):
        foto = st.file_uploader("Upload Gambar", type=["jpg", "jpeg", "png"])
        if foto is not None:
            with open("profile_photo.jpg", "wb") as f:
                f.write(foto.read())
            st.success("Foto berhasil disimpan.")

    with st.expander("Keahlian"):
        if "skill_data" not in st.session_state:
            st.session_state.skill_data = data["skills"] if data["skills"] else []

        new_skills = []
        remove_indexes = []

        for i, skill in enumerate(st.session_state.skill_data):
            nama_skill, nilai = skill.split(":") if ":" in skill else (skill, "50")
            input_nama = st.text_input(f"Nama Keahlian {i+1}", value=nama_skill.strip(), key=f"skill_nama_{i}")
            input_nilai = st.slider(f"Skor (%) {i+1}", 0, 100, int(nilai.strip()), key=f"skill_nilai_{i}")
            if st.button("Hapus Keahlian", key=f"hapus_{i}"):
                remove_indexes.append(i)
            new_skills.append(f"{input_nama}: {input_nilai}")

        for idx in sorted(remove_indexes, reverse=True):
            new_skills.pop(idx)

        if st.button("Tambah Keahlian Baru"):
            new_skills.append("Keahlian Baru: 50")
            st.session_state.skill_data = new_skills
            st.rerun()

        st.session_state.skill_data = new_skills

    with st.expander("Pengalaman"):
        new_judul = st.text_input("Judul Pengalaman")
        new_tahun = st.text_input("Tahun")
        new_desc = st.text_area("Deskripsi Pengalaman")
        if st.button("Tambah Pengalaman"):
            if new_judul and new_tahun:
                data["pengalaman"].append({
                    "judul": new_judul,
                    "tahun": new_tahun,
                    "deskripsi": new_desc
                })
                st.success("Pengalaman ditambahkan!")

    with st.expander("Proyek Portofolio"):
        proj_judul = st.text_input("Judul Proyek")
        proj_tahun = st.text_input("Tahun Proyek")
        proj_desc = st.text_area("Deskripsi Proyek")
        proj_link = st.text_input("Link Proyek")
        proj_gambar = st.text_input("Link Gambar (URL)")
        if st.button("Tambah Proyek"):
            data["projects"].append({
                "judul": proj_judul,
                "tahun": proj_tahun,
                "deskripsi": proj_desc,
                "link": proj_link,
                "gambar": proj_gambar
            })
            st.success("Proyek ditambahkan!")

    st.markdown("### Semua pesan pengunjung kini disimpan di Google Sheets (worksheet 'Pesan Pengunjung').")

    if st.button("Simpan Semua Perubahan"):
        data["profile"]["nama"] = nama
        data["profile"]["deskripsi"] = deskripsi
        data["skills"] = new_skills
        data["Identitas"] = {
            "alamat": alamat,
            "jenis_kelamin": jenis_kelamin,
            "agama": agama,
            "tanggal_lahir": str(tanggal_lahir),
            "instagram": instagram,
            "linkedin": linkedin,
            "github": github
        }
        save_data(data)
        st.success("Data berhasil disimpan!")
