# key = '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'
key = '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'
# from sendgrid.helpers.mail import Mail
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_mail(recepient,subject,message):
    sg = sendgrid.SendGridAPIClient(api_key=key)

    message = Mail(
        from_email='agarjoshua@protonmail.com',
        to_emails=[recepient], # type: ignore
        subject=subject,
        html_content=message) # type: ignore
    try:
        sg = SendGridAPIClient(key)
        response = sg.send(message) # type: ignore
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
