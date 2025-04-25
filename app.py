import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["gcp_service_account"],
    scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
)
gc = gspread.authorize(credentials)
sheet = gc.open("Data Portofolio").worksheet("Pesan Pengunjung")
