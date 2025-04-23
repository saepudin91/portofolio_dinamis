import streamlit as st
import json
import os

def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return {
        "profile": {},
        "identitas": {},
        "skills": [],
        "pengalaman": []
    }

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

st.set_page_config(page_title="Portofolio", layout="wide")
st.markdown("""<style>body { background-color: #1e1e1e; color: white; }</style>""", unsafe_allow_html=True)

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
            st.image("profile_photo.jpg", width=150)

        st.markdown("### Identitas")
        identitas = data.get("identitas", {})
        st.markdown(f"*Alamat:* {identitas.get('alamat', '-')}")
        st.markdown(f"*Agama:* {identitas.get('agama', '-')}")
        st.markdown(f"*Jenis Kelamin:* {identitas.get('jk', '-')}")
        st.markdown(f"*Sosial Media:* {identitas.get('sosmed', '-')}")
        st.markdown(f"*Email:* {identitas.get('email', '-')}")
        st.markdown(f"*Nomor HP:* {identitas.get('hp', '-')}")

    with col2:
        st.title(data["profile"].get("nama", "Nama Belum Diisi"))
        st.write(data["profile"].get("deskripsi", "Deskripsi belum diisi"))

        st.subheader("Keahlian")
        for skill in data["skills"]:
            if ":" in skill:
                nama, nilai = skill.split(":")
                st.write(f"{nama.strip()} ({nilai.strip()}%)")
                try:
                    st.progress(int(nilai.strip()))
                except:
                    st.write(f"(Format salah: {skill})")
            else:
                st.write(skill)

        st.subheader("Pengalaman")
        for exp in data["pengalaman"]:
            st.write(f"- {exp['judul']} ({exp['tahun']})  \n  {exp['deskripsi']}")

elif mode == "Edit (Admin)":
    st.title("Mode Edit Portofolio")
    password = st.text_input("Masukkan Password Admin", type="password")
    if password != "admin123":
        st.warning("Masukkan password untuk mengakses mode edit.")
        st.stop()

    st.subheader("Profil")
    nama = st.text_input("Nama", value=data["profile"].get("nama", ""))
    deskripsi = st.text_area("Deskripsi", value=data["profile"].get("deskripsi", ""))

    st.subheader("Upload Foto Profil")
    foto = st.file_uploader("Upload Gambar", type=["jpg", "jpeg", "png"])
    if foto is not None:
        with open("profile_photo.jpg", "wb") as f:
            f.write(foto.read())
        st.success("Foto berhasil disimpan.")

    st.subheader("Identitas")
    alamat = st.text_input("Alamat", value=data.get("identitas", {}).get("alamat", ""))
    agama = st.text_input("Agama", value=data.get("identitas", {}).get("agama", ""))
    jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"], index=0 if data.get("identitas", {}).get("jk", "Laki-laki") == "Laki-laki" else 1)
    sosmed = st.text_input("Sosial Media", value=data.get("identitas", {}).get("sosmed", ""))
    email = st.text_input("Email", value=data.get("identitas", {}).get("email", ""))
    hp = st.text_input("Nomor HP", value=data.get("identitas", {}).get("hp", ""))

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
    if st.button("Tambah"):
        if new_judul and new_tahun:
            data["pengalaman"].append({
                "judul": new_judul,
                "tahun": new_tahun,
                "deskripsi": new_desc
            })
            st.success("Pengalaman ditambahkan!")

    if st.button("Simpan Semua Perubahan"):
        data["profile"]["nama"] = nama
        data["profile"]["deskripsi"] = deskripsi
        data["skills"] = new_skills
        data["identitas"] = {
            "alamat": alamat,
            "agama": agama,
            "jk": jk,
            "sosmed": sosmed,
            "email": email,
            "hp": hp
        }
        save_data(data)
        st.success("Data berhasil disimpan!")

    if st.checkbox("Lihat Semua Pengalaman Saat Ini"):
        for i, exp in enumerate(data["pengalaman"]):
            st.write(f"{i+1}. {exp['judul']} ({exp['tahun']})")
