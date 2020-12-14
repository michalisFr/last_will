from last_will.emails import send_email
from twilio.rest import Client
from pathlib import Path
from datetime import date, datetime
import json
from crontab import CronTab


class Check:
    def __init__(self, last_check_in, deadline=None, warning_sent=False):
        self.last_check_in = last_check_in  # The last day last_will.py was run
        self.deadline = deadline  # The deadline datetime, if more than 30 have passed
        self.warning_sent = warning_sent  # True if a warning about deadline has already been sent

        try:
            with open('files/parameters.json') as params_file:
                parameters = json.loads(params_file.read())
        except OSError as e:
            print(f"Fatal error. Couldn't open parameters.json. Error: {e}")
            exit(1)

        self.sender_name = parameters['sender_name']
        self.recipient_email = parameters['recipient_email']
        self.subject = parameters['subject']
        self.unencrypted_message = parameters['unencrypted_message']

        try:
            with open('files/auth.json', 'r') as auth_file:
                auth = json.loads(auth_file.read())
        except OSError as e:
            print(f"Fatal error. Couldn't open auth.json. Error: {e}")
            exit(1)

        self.email = auth['email']
        self.email_pwd = auth['email_pwd_secret']
        self.your_email = auth['your_email']
        self.your_phone = auth['your_phone']
        self.twilio_phone = auth['twilio_phone']
        self.account_sid = auth['account_sid_secret']
        self.auth_token = auth['auth_token_secret']

    def dead(self):
        """Function to send the email to the designated recipient if you don't check in after the deadline has passed"""

        encrypted_file = ''
        for file in Path('files').iterdir():
            if file.suffix == '.gpg':
                encrypted_file = str(file)

        if encrypted_file == '':
            print("Fatal error. Didn't find an encrypted file in folder './files/")
            exit(1)

        send_email(self.sender_name, self.recipient_email,
                   self.email, self.email_pwd,
                   encrypted_file, self.subject, self.unencrypted_message)

        print("\nEmail with important info sent. Rest in peace, your money is in good hands\n")

        # Remove the cron job. No point in checking any longer.
        my_cron = CronTab(user=True)
        my_cron.remove_all(comment='check in')

        exit(0)

    def send_warning(self):
        """Function to send warnings to email and optionally as SMS,
        when at least 30 days have passed since the last check in"""

        # Check whether all the necessary parameters for SMS are present
        if self.your_phone != '' and self.twilio_phone != '' and self.account_sid != '' and self.auth_token != '':
            client = Client(self.account_sid, self.auth_token)

            try:
                sms = client.messages.create(
                    body="""Last will: It was at least 30 days since your last check in. 
                            This is a reminder to check in in the next 24 hours.""",
                    from_=self.twilio_phone,
                    to=self.your_phone)
                sms
                print("\nSMS sent")
            except Exception as e:
                print(f"An error occurred while trying to send the SMS. Error: {e}")

        else:
            print("\nMissing SMS parameters. SMS not sent")

        # Check whether all the necessary parameters for email are present
        if self.sender_name != '' and self.recipient_email != '' and self.email != '' and self.email_pwd != '':
            message = f"""It has been at least 30 days since you last checked in. 
You need to check in in the next 24 hours.\n
Otherwise at {self.deadline} the email with the important info will be sent to the designated recipient.\n
In order to reset simply go to the working directory and run ./last_will.sh"""

            # send_email will return 0 if everything went ok, otherwise it will return an error message
            status = send_email(self.sender_name, self.your_email,
                                self.email, self.email_pwd,
                                subject='Last will: Reminder to check in', unencrypted_message=message)

            if status != 0:
                print(status)
                exit(1)
            else:
                print("Email sent\n")

                print(f"You have until {self.deadline} to check in. "
                      f"In order to do that simply go to the working directory and run ./last_will.sh\n")
        else:
            print("Missing email parameters. Email not sent.\n")
            exit(1)


if __name__ == '__main__':
    if Path('files/check_in.json').exists():
        try:
            with open('files/check_in.json', 'r') as check_in_file:
                check_in_info = json.loads(check_in_file.read())
        except OSError as e:
            print(f"Fatal error. Couldn't open check_in.json. Error: {e}")
            exit(1)

        try:
            last_check_in = datetime.strptime(check_in_info['last_check_in'], "%Y-%m-%d").date()
        except ValueError as e:
            print(f"Fatal error. The last check in date is not in the right format. Error: {e}")
            exit(1)

        days_since_check_in = (date.today() - last_check_in).days

        checker = Check(last_check_in)

        if days_since_check_in > 30:
            # If there's no deadline key in check_in.json create it and put the deadline 24 hours from now.
            if 'deadline' not in check_in_info.keys():
                deadline = datetime.now().replace(day=date.today().day + 1, microsecond=0)
                check_in_info['deadline'] = str(deadline)

                try:
                    with open('files/check_in.json', 'w') as check_in_file:
                        check_in_file.write((json.dumps(check_in_info)))
                except OSError as e:
                    print(f"Fatal error. Couldn't open check_in.json to write the deadline. Error: {e}")

            # If a deadline has already been set, read it from the file and set the warning_sent flag to true
            # so that no more warnings are sent.
            else:
                deadline = datetime.strptime(check_in_info['deadline'], "%Y-%m-%d %H:%M:%S")
                checker.warning_sent = True

            checker.deadline = deadline

            if deadline < datetime.now():  # If the deadline has been passed, send the private info email
                checker.dead()
            elif not checker.warning_sent:  # Else if not passed and no warning has been sent, send the warning
                checker.send_warning()
            else:
                print("Warning already sent")

        # If last check in was less than 30 days ago, simply let the user know.
        else:
            print(f"You checked in {days_since_check_in} days ago. You have {30 - days_since_check_in} "
                  f"days more before you'll need to check in again.")

    else:
        print("There is no check_in.json file. Please run ./last_will.sh and fill out the relevant info")
