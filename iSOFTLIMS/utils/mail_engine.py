
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

# recepient=email
# subject='Password Reset'
# reset_link = 'htemsknshns.com'
# message=f'Click the link to reset your password:{reset_link}'

def send_mail(recepient,subject,message):
    message = Mail(
        from_email=From('ilims@isoftsystems.co.ke'),
        to_emails=To(recepient),
        subject=Subject(subject),
        plain_text_content=PlainTextContent(message),
        # html_content=Content('<strong>and easy to do anywhere, even with Python</strong>')
    )
    try:
        sg = SendGridAPIClient(api_key='EMAIL_HOST_PASSWORD')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

# send_mail('joshuaagarjj@gmail.com','Hello','Hello from the other side')