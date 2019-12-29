from pprint import pprint as print
# google sheets imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# sendgrid imports
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Bcc, Mail

# markdown
import misaka as m

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")


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
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    for email in to_emails:
        message = Mail(
            from_email="klawlor419@gmail.com",
            to_emails=[email]
        )
        message.dynamic_template_data = {
            "email_body": html_content,
            "subject": subject,
        }
        message.template_id = "d-4c873951ee8342d18507ac1c81050663"
        try:
            resp = sg.send(message)
            print(resp.status_code)
        except Exception as exc:
            print(exc.to_dict)


if __name__ == "__main__":
    gc = client()
    ss = spreadsheet(gc, "My Mailing List Sheet") 
    wks = ss.sheet1

    to_emails = list(emails(wks))
    subject = "Welcome!"
    html_content = render("posts/my-first-post.md")
    print(html_content)

    send_email(subject, html_content, to_emails)
