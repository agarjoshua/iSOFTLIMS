# key = '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'
key = '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'
# from sendgrid.helpers.mail import Mail
# import sendgrid
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

# def send_mail(recepient,subject,message):
#     sg = sendgrid.SendGridAPIClient(api_key=key)

#     message = Mail(
#         from_email='agarjoshua@protonmail.com',
#         to_emails=recepient, # type: ignore
#         subject=subject,
#         html_content=message) # type: ignore
#     try:
#         sg = SendGridAPIClient(key)
#         response = sg.send(message) # type: ignore
#         print(response.status_code)
#         print(response.body)
#         print(response.headers)
#     except Exception as e:
#         print(e)

# def send_mail():
#     key = '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'
#     # if isinstance(recepient, list):
#     #     recepient = recepient
#     # else:
#     #     recepient = [recepient]

#     mail = Mail(
#         from_email='agarjoshua@protonmail.com',
#         to_emails='joshuaagarjj@gmail.com',
#         subject="subject",
#         html_content="message",
#     )

#     sg = SendGridAPIClient(api_key=key)
#     sg.send(mail)

# send_mail()

# message = Mail(
#     from_email='agarjoshua@protonmail.com',
#     to_emails='joshuaagarjj@gmail.com',
#     subject='Sending with Twilio SendGrid is Fun',
#     html_content='<strong>and easy to do anywhere, even with Python</strong>')
# try:
#     sg = SendGridAPIClient(api_key='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')
#     response = sg.send(message)
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
# except Exception as e:
#     print(e.message)
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

# recepient=email
# subject='Password Reset'
# reset_link = 'htemsknshns.com'
# message=f'Click the link to reset your password:{reset_link}'

def send_mail(recepient,subject,message):
    message = Mail(
        from_email=From('agarjoshua@protonmail.com'),
        to_emails=To(recepient),
        subject=Subject(subject),
        plain_text_content=PlainTextContent(message),
        # html_content=Content('<strong>and easy to do anywhere, even with Python</strong>')
    )
    try:
        sg = SendGridAPIClient(api_key='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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

# send_mail(recepient,subject,message)