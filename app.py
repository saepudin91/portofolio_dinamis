import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

# Scope untuk akses Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials dari st.secrets
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["gcp_service_account"], scope
)

client = gspread.authorize(creds)

# Buka spreadsheet
sheet = client.open("Data Portofolio").worksheet("Pesan Pengunjung")
