import smtplib
from email.message import EmailMessage
from pathlib import Path


def send_email(sender, receiver_address, sender_address, password, content_file=None,
               subject=None, unencrypted_message=None):
    """This function is responsible for sending the emails, both warning and final"""
    email = EmailMessage()
    email['from'] = sender
    email['to'] = receiver_address
    email['subject'] = subject

    if unencrypted_message is not None:
        email.set_content(unencrypted_message, 'text')

    if content_file is not None:
        email.make_mixed()

        try:
            with open(content_file, 'rb') as attachment:
                email.add_attachment(attachment.read(), maintype='application', subtype='octate-stream', filename=Path(content_file).name)
        except OSError as e:
            return f"Fatal error. Unable to open or attach the encrypted file: {e}"

    try:
        with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(sender_address, password)
            smtp.send_message(email)
            return 0
    except smtplib.SMTPException as e:
        return f"Sending email failed: {e}"


if __name__ == '__main__':
    print("If you want to run this script standalone, edit it and provide the necessary parameters to the function call")