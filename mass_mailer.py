# google sheets imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# sendgrid imports
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# markdown
import misaka as m


def client():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'My Mailing List-d357f4649475.json',
        scope
    )
    gc = gspread.authorize(credentials)
    return gc


def spreadsheet(client, name):
    return client.open(name)


def emails(worksheet):
    for row in worksheet.get_all_records():
        yield row["Email Address"]


def render(filename):
    with open(filename, "r") as fp:
        return m.html(fp.read())


def send_email(subject, html_content, to_emails):
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    message = Mail(
        from_email="wgwz@pm.me",
        to_emails=to_emails,
        subject=subject,
        html_content=html_content,
    )
    resp = sg.send(message)
    print(resp.status_code)
    print(resp.body)
    print(resp.headers)


if __name__ == "__main__":
    gc = client()
    ss = spreadsheet(gc, "My Mailing List Sheet") 
    wks = ss.sheet1

    to_emails = list(emails(wks))
    subject = "Welcome!"
    html_content = render("posts/my-first-post.md")
    print(html_content)

    send_email(subject, html_content, to_emails)
