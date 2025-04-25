import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
gc = gspread.authorize(credentials)

# Akses sheet
sheet = gc.open("Data Portofolio").worksheet("Pesan Pengunjung")
