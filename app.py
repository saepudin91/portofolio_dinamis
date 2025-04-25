import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Load dari secrets
gcp_info = st.secrets["gcp_service_account"]
gcp_info = {k: v for k, v in gcp_info.items()}
gcp_info["private_key"] = gcp_info["private_key"].replace("\\n", "\n")  # safety

# Setup credentials dan client
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(gcp_info, scope)
client = gspread.authorize(creds)
