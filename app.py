import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Ambil JSON dari secrets
gcp_json = os.environ.get("GCP_SERVICE_ACCOUNT")
service_account_info = json.loads(gcp_json)

# Buat credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)

# Test koneksi
spreadsheet = client.open("Data Portofolio")
worksheet = spreadsheet.sheet1
print("Isi A1:", worksheet.acell("A1").value)
