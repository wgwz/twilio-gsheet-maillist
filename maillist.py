import argparse

# config
from dotenv import load_dotenv

# google sheets imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# sendgrid imports
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Bcc, Mail

# markdown
import markdown2 as m


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


def render(fp):
    return m.markdown(fp.read())


def send_email(from_addr, subject, html_content, to_emails):
    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    unsubscribe = f"<p>To unsubscribe email: {from_addr}</p>"
    for email in to_emails:
        message = Mail(
            subject=subject,
            from_email=from_address,
            html_content=f"{html_content}\n{unsubscribe}",
            to_emails=[email],
        )
        try:
            resp = sg.send(message)
        except Exception as exc:
            print(exc)


if __name__ == "__main__":

    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--markdown",
        "-m",
        required=True,
        help="Markdown content for post.",
        type=argparse.FileType("r"),
    )
    parser.add_argument("--subject", "-s", required=True, help="Subject for the post.")

    # config values
    cred_file_path = os.getenv("GOOGLE_CRED_FILE")
    spreadsheet_name = os.getenv("SPREADSHEET_NAME")
    from_address = os.getenv("FROM_ADDRESS")

    # cli arguments
    args = parser.parse_args()

    gc = client(cred_file_path)
    ss = spreadsheet(gc, spreadsheet_name)
    wks = ss.sheet1

    to_emails = list(emails(wks))
    html_content = render(args.markdown)

    send_email(from_address, args.subject, html_content, to_emails)
