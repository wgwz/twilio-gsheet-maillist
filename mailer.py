# sendgrid imports
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Bcc, Mail


def send_email(from_addr, subject, html_content, to_emails, api_key):
    sg = SendGridAPIClient(api_key)
    unsubscribe = f"<a href='mailto:{from_addr}?subject=Unsubscribe'>Unsubscribe</a>"
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
