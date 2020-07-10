# last_will
last_will is a program that allows you to send an encrypted file with private information (passwords, PIN numbers etc) to a predesignated recipient, in case of your untimely death.

The recipient needs to have a PGP Public/Private key pair. The file is encrypted with the recipient's Public Key and that ensures that only them can decrypt it and read the contents. The file can be in any format (doc, pdf, txt, etc).

## Setup

Clone the repo in your working folder:

`git clone https://github.com/michalisFr/last_will.git`

Then make setup.sh executable and run it:

```
cd last_will
chmod +x setup.sh
./setup.sh
```
This will run pipenv and install all the necessary dependencies, then open the GUI.

## How it works

The concept is simple. 

You create a file where you include information that your close ones will need in case of your untimely death. **IMPORTANT: For security reasons, it is highly recommended that you don't keep this (unencrypted) file on your computer**

You coordinate with a close friend or relative who will be the recipient of this file and they provide you with their PGP Public key. last_will will encrypt your file with this Public key, ensuring that only them can read it. 

Then you give last_will all the necessary information (like recipient's email, your email, the public key file etc) and forget about it. Every 30 days you will receive an email (and optionally a text message) asking you to check in. In that case all you need to do is run last_will. Open terminal, go to the working directory and run:
```
./last_will.sh
``` 
If you don't check in within 24 hours after you receive the warning, the file will be sent to the recipient, since it's assumed you have left this vain world.

All the recipient needs to do then is decrypt the file with their Private key and rad the information you left for them.

## GUI

last_will comes with a GUI to enter all the necessary information.

* **Name to appear as sender:** This is the name that will appear to the recipient as the sender of the email
* **Recipient's email:** The email where the private information will be sent
* **Email subject:** The subject of the email
* **Unencrypted message:** A message you might want to add in plain text to accompany your file. This message will appear in the email's body.
* **File to encrypt:** The file that contains your private information. 
* **Recipient's PUBLIC key:** An .asc file that contains the recipients PGP Public key.

* **Email to send from:** The email address used to send the email
* **Email's password:** The password to that email. If you have enabled 2FA you will need a token instead of your usual password. Also, for Gmail (and perhaps other providers) you may need to allow insecure apps.
* **Your email:** The email to which you wish to receive the notification to check in

Feel out the following if you have a Twilio account. 
* **Your phone number:** You will receive a text message to this phone number when it's time to check in. If your Twilio account if free, you'll need to verify this number in order to be able to receive messages.
* **Your Twilio phone number:** The phone number of your Twilio account. 
* **Your Twilio account ID:** Your Twilio account ID
* **Your Twilio Auth token:** Your Twilio Auth token

Once all the information is filled out click on on **Update**. The encrypted file and all the information you filled out will be stored in the `./files` folder.

## Scheduling

The command that needs to be run daily to check whether you need to check in is `pipenv run python3 check_in.py`.

There's a `scedule_cron.py` which you can use (on Linux and macOS) to create a cron job that will do that for you.
```
./schedule_cron.py SHELL=<shell> PATH=<path> MAILTO=<user> TIME=<scheduled time>
```  
All the parameters are optional but, if used, must be given in the above format. 

`SHELL` If you want cron to run in a different shell than the default (/bin/sh)\
`PATH` If you want to set a custom PATH for cron. Cron runs with an empty Path basically (/usr/bin:/bin)\
`MAILTO` You can set this to `""` so that cron doesn't send you mails. Or you can set a different user on your machine.\
`TIME` The time you want the script to run every day. It must be in format `HH:MM`. The default is 12:00.

**If you don't use this script then you need to schedule for `pipenv run python3 sheck_in.py` to run every day, otherwise the whole thing won't work**
   
The computer needs to be running (and not in sleep mode) when the cron job is scheduled to run, otherwise it won't run for that day. Setting up the program on a computer that's always on or on a server is a good idea.

Alternatively you can schedule an event to wake-up your computer daily on the time you've set the cron job. For a laptop (on MacOS at least), the lid needs to be open for the event to run.

## Security

**The original (unencrypted) file should not be kept on your computer.** Ideally you should delete it after it's encrypted and empty the Trash. If you think you might need to make changes in the future, keep it on a USB drive that's used specifically for that purpose and hide it somewhere safe.

It's also not a good idea to keep all your eggs in one basket, even if the file is encrypted. Give information that alone can't give access to something. 

For example, the password to your safe also requires access to the safe itself. Your master password for your password manager probably also requires an additional Secret Key and 2FA, which can be kept in your safe and on your phone respectively. Your computer password is useless without the computer and same goes for your phone's PIN.

On the other hand, don't include cryptocurrency Private Keys or seeds, for example. Put these in your safe of bank vault and tell them how to access them.

**IMPORTANT:** Keep in mind that the credentials to your email and Twilio account are stored in plain text. Unfortunately they can't be encrypted because then `check_in.py` wouldn't be able to access them and send the emails and text message automatically. So make sure that your computer is free of malware. If you don't feel comfortable storing this information on your computer, **don't use this program!**

## Disclaimer

**Please make sure you understand how this program works and the security risks involved. I can't be held responsible if your private information or credentials fall into the wrong hands!** 