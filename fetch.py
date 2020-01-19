# google sheets imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def client(cred_file_path):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        cred_file_path, scope
    )
    gc = gspread.authorize(credentials)
    return gc


def spreadsheet(client, name):
    return client.open(name)


def emails(worksheet):
    for row in worksheet.get_all_records():
        if row["Email Address"]:
            yield row["Email Address"]
