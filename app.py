import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Portofolio", layout="centered")

# Koneksi Google Sheets
def connect_sheet(sheet_name):
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(st.secrets["gcp_service_account"]), scope)
    client = gspread.authorize(creds)
    return client.open("Data Portofolio").worksheet(sheet_name)

# Inisialisasi header jika sheet kosong
def init_table_if_empty(sheet_name, headers):
    sheet = connect_sheet(sheet_name)
    values = sheet.get_all_values()
    if not values:
        sheet.append_row(headers)

# Load data profil dari Google Sheets
def load_data():
    try:
        sheet = connect_sheet("Data")
        rows = sheet.get_all_records()
        if rows:
            return rows[0]
        else:
            return {}
    except:
        return {}

# Simpan data profil ke Google Sheets
def save_data(data):
    sheet = connect_sheet("Data")
    sheet.clear()
    headers = list(data.keys())
    values = list(data.values())
    sheet.append_row(headers)
    sheet.append_row(values)

# Simpan pesan ke Google Sheets
def simpan_ke_google_sheet(nama, email, pesan):
    sheet = connect_sheet("Pesan Pengunjung")
    values = sheet.get_all_values()
    if not values or values[0] != ["Waktu", "Nama", "Email", "Pesan"]:
        sheet.insert_row(["Waktu", "Nama", "Email", "Pesan"], 1)
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([waktu, nama, email, pesan])

# Fungsi umum untuk data tabel (skills, pengalaman, proyek)
def load_table(sheet_name):
    sheet = connect_sheet(sheet_name)
    records = sheet.get_all_records()
    return pd.DataFrame(records)

def save_table(sheet_name, df):
    sheet = connect_sheet(sheet_name)
    sheet.clear()
    sheet.append_row(list(df.columns))
    for _, row in df.iterrows():
        sheet.append_row(row.tolist())

sheet_data = load_data()

# Sidebar
st.sidebar.title("Mode")
mode = st.sidebar.radio("Pilih mode:", ["Tampilan Publik", "Edit (Admin)"])

if mode == "Tampilan Publik":
    # Inisialisasi jika kosong
    init_table_if_empty("Skills", ["Skill", "Keterangan"])
    init_table_if_empty("Pengalaman", ["Judul", "Deskripsi"])
    init_table_if_empty("Proyek", ["Nama Proyek", "Detail"])

    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        .container-publik {
            max-width: 800px;
            margin: auto;
        }
        .custom-title {
            font-family: 'Poppins', sans-serif;
            font-size: 5vw;
            text-align: center;
            color: #2C3E50;
            font-weight: 600;
        }
        .custom-desc {
            font-family: 'Poppins', sans-serif;
            font-size: 3.5vw;
            text-align: center;
            color: #555;
        }
        .section-title {
            font-family: 'Poppins', sans-serif;
            font-size: 4vw;
            color: #34495E;
            font-weight: 600;
            border-bottom: 2px solid #ddd;
            padding-bottom: 0.2rem;
            margin-top: 2rem;
        }
        .section-entry {
            font-family: 'Poppins', sans-serif;
            font-size: 1rem;
            color: #333;
            margin-bottom: 0.5rem;
        }
        .hubungi {
            font-family: 'Poppins', sans-serif;
            font-size: 1rem;
            text-align: center;
            margin-top: 2rem;
        }
        @media (min-width: 768px) {
            .custom-title { font-size: 2.5vw; }
            .custom-desc { font-size: 1.5vw; }
            .section-title { font-size: 1.8vw; }
        }
        @media (max-width: 480px) {
            .custom-title { font-size: 7vw; }
            .custom-desc { font-size: 4.5vw; }
            .section-title { font-size: 5vw; }
        }
        </style>
        <div class="container-publik">
    """, unsafe_allow_html=True)

    st.image("profile_photo.jpg", use_container_width=True)
    st.markdown(f"<div class='custom-title'>{sheet_data.get('nama', 'Nama Belum Diisi')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='custom-desc'>{sheet_data.get('deskripsi', 'Deskripsi belum diisi')}</div>", unsafe_allow_html=True)

    for section, title in zip(["Skills", "Pengalaman", "Proyek"], ["🚀 Skills", "💼 Pengalaman", "📁 Proyek"]):
        df = load_table(section)
        if not df.empty:
            st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
            for i, row in df.iterrows():
                st.markdown(f"<div class='section-entry'><b>{row[0]}</b><br>{row[1]}</div>", unsafe_allow_html=True)

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
                st.success("Pesan berhasil dikirim!")
            except Exception as e:
                st.error(f"Gagal menyimpan pesan: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

elif mode == "Edit (Admin)":
    st.title("Mode Edit Portofolio")
    st.markdown("<div style='color:white;background-color:#1E90FF;padding:0.5rem;border-radius:5px;font-weight:bold;'>Admin Mode Aktif</div>", unsafe_allow_html=True)
    password = st.text_input("Masukkan Password Admin", type="password")
    if password != "admin123":
        st.warning("Masukkan password untuk mengakses mode edit.")
        st.stop()

    with st.form("form_edit"):
        nama = st.text_input("Nama", value=sheet_data.get("nama", ""))
        deskripsi = st.text_area("Deskripsi", value=sheet_data.get("deskripsi", ""))
        simpan = st.form_submit_button("Simpan Perubahan")
        if simpan:
            sheet_data["nama"] = nama
            sheet_data["deskripsi"] = deskripsi
            try:
                save_data(sheet_data)
                st.success("Data berhasil disimpan ke Google Sheets!")
            except Exception as e:
                st.error(f"Gagal menyimpan data: {e}")

    for section, headers in zip(
        ["Skills", "Pengalaman", "Proyek"],
        [["Skill", "Keterangan"], ["Judul", "Deskripsi"], ["Nama Proyek", "Detail"]]
    ):
        init_table_if_empty(section, headers)
        st.subheader(f"Edit {section}")
        df = load_table(section)
        edited_df = st.experimental_data_editor(df, num_rows="dynamic", use_container_width=True)
        if st.button(f"Simpan {section}"):
            try:
                save_table(section, edited_df)
                st.success(f"{section} berhasil disimpan!")
            except Exception as e:
                st.error(f"Gagal menyimpan {section}: {e}")

    st.subheader("Pesan dari Pengunjung")
    try:
        sheet_pesan = connect_sheet("Pesan Pengunjung")
        records = sheet_pesan.get_all_records()
        if records:
            df_pesan = pd.DataFrame(records)
            st.dataframe(df_pesan)
        else:
            st.info("Belum ada pesan masuk.")
    except Exception as e:
        st.error(f"Gagal memuat pesan: {e}")
