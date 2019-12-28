# google sheets imports


# sendgrid imports
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1LrhTBlWE4me97Zt2LnH7Q72x_fBvkedaOomzNXK8DY0"
SAMPLE_RANGE_NAME = "A:B"


def gsheet():
    raise NotImplementedError


def emails():
    # get the emails from the spreadsheet
    emails = []
    for row in result["values"][1:]:
        try:
            emails.append(row[1])
        except IndexError:
            pass
    print(emails)


def blast_off():
    # set up sendgrid and blastoff the emails
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    message = Mail(
        from_email="wgwz@pm.me",
        to_emails=emails,
        subject="This is a new post",
        plain_text_content="Helloworld",
    )
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    resp = sg.send(message)
    print(resp.status_code)
    print(resp.body)
    print(resp.headers)

if __name__ == "__main__":
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'My Mailing List-d357f4649475.json',
        scope
    )
    
    gc = gspread.authorize(credentials)
    
    wks = gc.open("My Mailing List Sheet").sheet1
    print(wks)
    import pdb; pdb.set_trace()
