import streamlit as st
import json
import os

st.set_page_config(page_title="Portofolio", layout="wide")

def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return {"profile": {}, "skills": [], "pengalaman": [], "identitas": {}, "projects": []}

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

st.sidebar.title("Mode")
mode = st.sidebar.radio("Pilih mode:", ["Tampilan Publik", "Edit (Admin)"])

data = load_data()

if not os.path.exists("profile_photo.jpg"):
    with open("profile_photo.jpg", "wb") as f:
        pass

if mode == "Tampilan Publik":
    col1, col2 = st.columns([1, 3])

    with col1:
        if os.path.exists("profile_photo.jpg") and os.path.getsize("profile_photo.jpg") > 0:
            st.image("profile_photo.jpg", width=180)
        else:
            st.write("Foto belum diunggah")

    with col2:
        st.title(data["profile"].get("nama", "Nama Belum Diisi"))
        st.write(data["profile"].get("deskripsi", "Deskripsi belum diisi"))

    st.markdown("---")
    st.subheader("Keahlian")
    for skill in data["skills"]:
        if ":" in skill:
            nama, nilai = skill.split(":")
            st.write(f"{nama.strip()}** ({nilai.strip()}%)")
            try:
                st.progress(int(nilai.strip()))
            except:
                st.write(f"(Format salah: {skill})")
        else:
            st.write(skill)

    st.markdown("---")
    st.subheader("Pengalaman")
    for exp in data["pengalaman"]:
        st.markdown(f"{exp['judul']}** ({exp['tahun']})  \n{exp['deskripsi']}")

    st.markdown("---")
    st.subheader("Portofolio Proyek")
    for proj in data.get("projects", []):
        st.markdown(f"### {proj['judul']} ({proj['tahun']})")
        st.image(proj["gambar"], width=300)
        st.write(proj["deskripsi"])
        if proj.get("link"):
            st.markdown(f"[Lihat Proyek]({proj['link']})", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Hubungi Saya")
    st.markdown("[WhatsApp](https://wa.me/087810059643)")

elif mode == "Edit (Admin)":
    st.title("Mode Edit Portofolio")
    password = st.text_input("Masukkan Password Admin", type="password")
    if password != "admin123":
        st.warning("Masukkan password untuk mengakses mode edit.")
        st.stop()

    st.subheader("Profil")
    nama = st.text_input("Nama", value=data["profile"].get("nama", ""))
    deskripsi = st.text_area("Deskripsi", value=data["profile"].get("deskripsi", ""))

    st.subheader("Identitas")
    alamat = st.text_input("Alamat", value=data["profile"].get("alamat", ""))
    jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"], index=0 if data["profile"].get("jenis_kelamin") == "Laki-laki" else 1)
    agama = st.text_input("Agama", value=data["profile"].get("agama", ""))
    tanggal_lahir = st.date_input("Tanggal Lahir")
    instagram = st.text_input("Instagram", value=data["profile"].get("instagram", ""))
    linkedin = st.text_input("LinkedIn", value=data["profile"].get("linkedin", ""))
    github = st.text_input("GitHub", value=data["profile"].get("github", ""))

    st.subheader("Upload Foto Profil")
    foto = st.file_uploader("Upload Gambar", type=["jpg", "jpeg", "png"])
    if foto is not None:
        with open("profile_photo.jpg", "wb") as f:
            f.write(foto.read())
        st.success("Foto berhasil disimpan.")

    st.subheader("Keahlian")
    if "skill_data" not in st.session_state:
        st.session_state.skill_data = data["skills"] if data["skills"] else []

    new_skills = []
    remove_indexes = []

    for i, skill in enumerate(st.session_state.skill_data):
        nama_skill, nilai = skill.split(":") if ":" in skill else (skill, "50")
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            input_nama = st.text_input(f"Nama Keahlian {i+1}", value=nama_skill.strip(), key=f"skill_nama_{i}")
        with col2:
            input_nilai = st.slider(f"Skor (%) {i+1}", 0, 100, int(nilai.strip()), key=f"skill_nilai_{i}")
        with col3:
            if st.button("Hapus", key=f"hapus_{i}"):
                remove_indexes.append(i)
        new_skills.append(f"{input_nama}: {input_nilai}")

    for idx in sorted(remove_indexes, reverse=True):
        new_skills.pop(idx)

    if st.button("Tambah Keahlian Baru"):
        new_skills.append("Keahlian Baru: 50")
        st.session_state.skill_data = new_skills
        st.rerun()

    st.session_state.skill_data = new_skills

    st.subheader("Tambah Pengalaman Baru")
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

    st.subheader("Tambah Proyek Portofolio")
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

    if st.checkbox("Lihat Semua Pengalaman Saat Ini"):
        for i, exp in enumerate(data["pengalaman"]):
            st.write(f"{i+1}. {exp['judul']} ({exp['tahun']})")
