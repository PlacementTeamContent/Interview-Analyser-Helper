import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import json

class GoogleSheetsCRUD:
    def __init__(self, credentials_json, sheet_name, sub_sheet_name):
        """
        Initializes the GoogleSheetsCRUD class with Google Sheets authentication.

        :param credentials_json: Path to the Google API credentials JSON file.
        :param sheet_name: Name of the Google Sheet.
        :param sub_sheet_name: Name of the sub-sheet (worksheet) inside the Google Sheet.
        """
        self.sheet_name = sheet_name
        self.sub_sheet_name = sub_sheet_name
        self.client = self.authenticate_google_sheets(credentials_json)
        self.sheet = self.client.open(sheet_name).worksheet(sub_sheet_name)

    def authenticate_google_sheets(self, credentials_json):
        """Authenticate and return the Google Sheets client."""
        google_credentials_json = st.secrets["google_sheets"]["credentials"]
        credentials_dict = json.loads(google_credentials_json)
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
        client = gspread.authorize(creds)
        return client

    def read_all_data(self):
        """Read all data from the sub-sheet."""
        data = self.sheet.get_all_records()
        return data

    def read_row(self, row_number):
        """Read data from a specific row in the sub-sheet."""
        row_data = self.sheet.row_values(row_number)
        return row_data

    def read_column(self, col_number):
        """Read data from a specific column in the sub-sheet."""
        column_data = self.sheet.col_values(col_number)
        return column_data

    def write_to_row(self, row_number, data):
        """Write data to a specific row in the sub-sheet."""
        self.sheet.update(f"A{row_number}:Z{row_number}", [data])

    def append_to_sheet(self, data):
        """Append data to the sub-sheet."""
        self.sheet.append_row(data)

    def update_cell(self, cell, value):
        """Update a specific cell in the sub-sheet."""
        self.sheet.update(cell, value)

    def delete_row(self, row_number):
        """Delete a specific row in the sub-sheet."""
        self.sheet.delete_rows(row_number)

    def update_row(self, row_number, data):
        """Update a specific row in the sub-sheet."""
        self.sheet.update(f"A{row_number}:Z{row_number}", [data])

    def delete_rows_in_range(self, start_row, end_row):
        """Delete rows in a given range (from start_row to end_row)."""
        for row in range(start_row, end_row + 1):
            self.sheet.delete_rows(start_row)
