# last_will
last_will is a program that allows you to send an encrypted file with private information (passwords, PIN numbers etc) to a predesignated recipient, in case of your untimely death.

The recipient needs to have a PGP Public/Private key pair. The file is encrypted with the recipient's Public Key and that ensures that only them can decrypt it and read the contents. The file can be in any format (doc, pdf, txt, etc).

The intended usage is as a stand-alone utility and not as a library to import to other projects.
## Setup

You usually will want to install `last_will` in a directory other than `site-packages` that pip uses to install packages, for easy access. 

In order to do that, type:
```
pip install -t <installation_dir> --no-deps last-will
pip install last-will
```
For example:
```
pip install -t ~/last_will --no-deps last-will
pip install last-will
```
This actually installs `last_will` both in the `<installation_dir>` and in `site-packages`, but it prevents the dependencies to be installed in the `<installation_dir>`.
#### Note about Tkinter
This program uses the `tkinter` library to build the GUI. If you encounter an import error regarding `tkinter`, you need to install it on your system. Please try the following:

**For MacOS**
```
brew install tcl-tk
``` 
**For Ubuntu**
```
sudo apt-get install tk-dev
```
**pynev**

Please note that if you're using `pyenv` you may encounter version incompatibility issues with `tkinter`. It is recommended that you use `last_will` with your system version of Python. If you're interested in making `tkinter` work with `pyenv` have a look at this thread:\
https://github.com/pyenv/pyenv/issues/1375
## Usage

To open the GUI, first navigate to the folder:
```
cd <installation_dir>/last_will
```
and then run:

```
python3 last_will.py
```
After you fill out the necessary information, run the scheduler (while in the same folder):
```
python3 schedule_cron.py
```
When you need to check in every month, simply navigate to the above folder and open the GUI in the same way. If you don't want to change anything, simply click **Quit**, otherwise update the information you want, click **Update** and then **Quit**.

Below you'll find more details on the usage and scheduling.
## How it works

The concept is simple. 

You create a file where you include information that a trusted person will need in case of your untimely death. **IMPORTANT: For security reasons, it is highly recommended that you don't keep this (unencrypted) file on your computer**

You coordinate with a close friend or relative who will be the recipient of this file and they provide you with their PGP Public key. `last_will` will encrypt your file with this Public key, ensuring that only them can read it. 

Then you give `last_will` all the necessary information (like recipient's email, your email, the public key file etc) and forget about it. Every 30 days you will receive an email (and optionally a text message) asking you to check in. In that case all you need to do is run `last_will`. 

To do that, open terminal and type:
```
cd <installation_dir>/last_will
python3 last_will.py
``` 
If you don't check in within 24 hours after you receive the warning, the file will be sent to the recipient, since it's assumed you have left this vain world.

All the recipient needs to do then is decrypt the file with their Private key and read the information you left for them.

## GUI

`last_will` comes with a GUI to enter all the necessary information.

* **Name to appear as sender:** This is the name that will appear to the recipient as the sender of the email
* **Recipient's email:** The email where the private information will be sent
* **Email subject:** The subject of the email
* **Unencrypted message:** A message you might want to add in plain text to accompany your file. This message will appear in the email's body.
* **File to encrypt:** The file that contains your private information. 
* **Recipient's PUBLIC key:** An .asc file that contains the recipient's PGP Public key.

* **Email to send from:** The email address used to send the email. It's a good idea to set up an email account specifically for this purpose.
* **Email's password:** The password to that email. If you have enabled 2FA you will need a token instead of your usual password. Also, for Gmail (and perhaps other providers) **you need to allow insecure apps**, otherwise the email won't be sent.
* **Your email:** The email to which you wish to receive the notification to check in

Fill out the following if you have a Twilio account. 
* **Your phone number:** You will receive a text message to this phone number when it's time to check in. If your Twilio account if free, you'll need to verify this number in order to be able to receive messages.
* **Your Twilio phone number:** The phone number of your Twilio account. 
* **Your Twilio account ID:** Your Twilio account ID
* **Your Twilio Auth token:** Your Twilio Auth token

Once all the information is filled out click on **Update**. The encrypted file and all the information you filled out will be stored in a `/files` folder, inside the package folder.

## Scheduling

The command that needs to be run daily to check whether you need to check in is: 
```
cd <installation_dir>/last_will && python3 check_in.py
```

There's a `scedule_cron.py` script which you can use (on Linux and macOS) to create a cron job that will do that for you.

First **make sure you navigate to the folder:** 
```
cd <installation_dir>/last_will
``` 
and then run:
```
python3 schedule_cron.py
```  
You can use the following optional parameters: 

`-s, --shell` If you want cron to run in a different shell than the default (/bin/sh)\
`-p, --path` If you want to set a custom PATH for cron. Cron runs with an empty Path basically (/usr/bin:/bin)\
`-m, --mailto` You can set this to `""` so that cron doesn't send you mails. Or you can set a different user on your machine. The default location is `/var/mail`. 
It is recommended that you leave that option to default and check the messages periodically (especially after the first use) to ensure that everything is working as expected.\
`-t, --time` The time you want the script to run every day. It must be in format `HH:MM`. The default is 12:00. \
`-d, --display` Display the current configuration and cron jobs (equivalent to `cronjob -l`) \
`-r, --remove` Delete the job.

**If you don't use this script then you need to schedule in some other way for `check_in.py` to run every day from the above folder, otherwise the whole thing won't work**
   
The computer needs to be running (and not in sleep mode) when the cron job is scheduled to run, otherwise it won't run for that day. Setting up the program on a computer that's always on or on a local server is a good idea (although you need to consider security, as sensitive information, eg. the email password, are stored locally)

Alternatively you can schedule an event to wake-up your computer daily on the time you've set the cron job. For a laptop (on MacOS at least), the lid needs to be open for the event to run.

## Security

**The original (unencrypted) file should not be kept on your computer.** Ideally you should delete it after it's encrypted and empty the Trash. If you think you might need to make changes in the future, keep it on a USB drive that's used specifically for that purpose and hide it somewhere safe.

It's also not a good idea to keep all your eggs in one basket, even if the file is encrypted. Give information that alone can't give access to something. 

For example, the password to your safe also requires access to the safe itself. Your master password for your password manager probably also requires an additional Secret Key and 2FA, which can be kept in your safe and on your phone respectively. Your computer password is useless without the computer and same goes for your phone's PIN.

On the other hand, don't include cryptocurrency Private Keys or seeds, for example. Put these in a safe or bank vault and tell them how to access them.

**IMPORTANT:** Keep in mind that the credentials to your email and Twilio account are stored in plain text. Unfortunately they can't be encrypted because then `check_in.py` wouldn't be able to access them and send the emails and text message automatically. So make sure that your computer is free of malware. If you don't feel comfortable storing this information on your computer, **don't use this program!**

## Disclaimer

**Please make sure you understand how this program works and the security risks involved. I can't be held responsible if your private information or credentials fall into the wrong hands!** 