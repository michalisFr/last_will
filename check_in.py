#!/usr/bin/env python
from emails import send_email
from twilio.rest import Client
from pathlib import Path
from datetime import date, datetime
import json


class Check:
    def __init__(self, last_check_in, deadline=None, warning_sent=False):
        self.last_check_in =last_check_in
        self.deadline = deadline
        self.warning_sent = warning_sent

        with open('./files/parameters.json') as params_file:
            parameters = json.loads(params_file.read())

        self.sender_name = parameters['sender_name']
        self.recipient_email = parameters['recipient_email']
        self.subject = parameters['subject']
        self.unencrypted_message = parameters['unencrypted_message']

        with open('./files/auth.json', 'r') as auth_file:
            auth = json.loads(auth_file.read())

        self.email = auth['email']
        self.email_pwd = auth['email_pwd_secret']
        self.your_phone = auth['your_phone']
        self.twilio_phone = auth['twilio_phone']
        self.account_sid = auth['account_sid_secret']
        self.auth_token = auth['auth_token_secret']

    def dead(self):
        print("\nI'm sorry you're dead\n")

        encrypted_file = ''
        for file in Path('./files').iterdir():
            if file.suffix == '.gpg':
                encrypted_file = str(file)

        send_email(self.sender_name, self.recipient_email,
                   self.email, self.email_pwd,
                   encrypted_file, self.subject, self.unencrypted_message)

        print("\nEmail with important info sent. Rest in peace, your money is in good hands\n")
        # cancel cron job

        exit()

    def send_warning(self):
        if self.your_phone != '' and self.twilio_phone != '' and self.account_sid != '' and self.auth_token != '':
            client = Client(self.account_sid, self.auth_token)

            sms = client.messages \
                .create(
                body="Last will: It was at least 30 days since your last check in. This is a reminder to check in in the next 24 hours.",
                from_=self.twilio_phone,
                to=self.your_phone
            )

            sms
            print("\nSMS sent")
        else:
            print("\nMissing SMS parameters. SMS not sent")

        if self.sender_name != '' and self.recipient_email != '' and self.email != '' and self.email_pwd != '':
            message = f'''It has been at least 30 days since you last checked in. You need to check in in the next 24 hours.\n
Otherwise at {self.deadline} the email with the important info will be sent to the designated recipient.\n
In order to reset simply run last_will.py'''

            send_email(self.sender_name, self.recipient_email,
                self.email, self.email_pwd,
                subject='Last will: Reminder to check in', unencrypted_message=message)

            print("Email sent\n")

            print(f"You have until {self.deadline} to check in. In order to do that simply run last_will.py\n")
        else:
            print("Missing email parameters. Email not sent.\n")


if __name__ == '__main__':
    if Path('./files/check_in.json').exists():
        with open('./files/check_in.json', 'r') as check_in_file:
            check_in_info = json.loads(check_in_file.read())

        last_check_in = datetime.strptime(check_in_info['last_check_in'], "%Y-%m-%d").date()

        days_since_check_in = (date.today() - last_check_in).days

        checker = Check(last_check_in)

        if days_since_check_in > 30:
            if 'deadline' not in check_in_info.keys():
                deadline = datetime.now().replace(day=date.today().day + 1, microsecond=0)
                check_in_info['deadline'] = str(deadline)
                with open('./files/check_in.json', 'w') as check_in_file:
                    check_in_file.write((json.dumps(check_in_info)))

            else:
                deadline = datetime.strptime(check_in_info['deadline'], "%Y-%m-%d %H:%M:%S")
                checker.warning_sent = True

            checker.deadline = deadline

            if deadline < datetime.now():
                checker.dead()
            elif not checker.warning_sent:
                checker.send_warning()
            else:
                print("Warning already sent")
        else:
            print(f"You checked in {days_since_check_in} days ago. You have {30 - days_since_check_in} days more before you'll need to check in again.")

    else:
        print("There is no check_in.json file. Please run last_will.py and fill out the relevant info")
