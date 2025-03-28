import gspread
from google.oauth2.service_account import Credentials

class GoogleSheet:
    def __init__(self, service_account_path):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_file(service_account_path, scopes=scopes)
        self.client = gspread.authorize(creds)
