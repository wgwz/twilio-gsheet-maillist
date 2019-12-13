# google sheets imports
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# sendgrid imports
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1LrhTBlWE4me97Zt2LnH7Q72x_fBvkedaOomzNXK8DY0'
SAMPLE_RANGE_NAME = 'A:B'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    print(result)

    # get the emails from the spreadsheet
    emails = []
    for row in result["values"][1:]:
        try:
            emails.append(row[1])
        except IndexError:
            pass
    print(emails)

    # set up sendgrid and blastoff the emails
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    message = Mail(
        from_email="wgwz@pm.me",
        to_emails=emails,
        subject="Test Mail",
        plain_text_content="Hello world",
    )
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    resp = sg.send(message)
    print(resp.status_code)
    print(resp.body)
    print(resp.headers)


if __name__ == '__main__':
    main()
