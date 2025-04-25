import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

def connect_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scope
    )
    client = gspread.authorize(credentials)
    sheet = client.open("Data Portofolio").worksheet(Pesan Pengunjung)
    return sheet
