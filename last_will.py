#!/usr/bin/env python
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from pathlib import Path
import json
from datetime import date
import file_encryption

class App:
    def __init__(self, root):
        root.title('Last Will')

        big_frame = ttk.Frame(root)
        big_frame.pack()

        left_frame = ttk.Frame(big_frame)
        right_frame = ttk.Frame(big_frame)
        left_frame.grid(row=0, column=0, sticky=N)
        right_frame.grid(row=0, column=1, sticky=N)

        self.left_labels = ["Name to appear as sender", "Recipient's email", "Email subject", "Unencrypted message",
                            "File to encrypt", "Recipient's PUBLIC Key"]
        self.left_entry_labels = ['sender_name', 'recipient_email', 'subject', 'unencrypted_message',
                                  'file_to_encrypt', 'pubkey_file']
        self.left_entries = self.labels_entries(left_frame, self.left_labels, self.left_entry_labels)
        self.entry_values = {}

        ttk.Button(left_frame, text='Browse', command=self.file_dialog1).grid(row=4, column=2, sticky='W')
        ttk.Button(left_frame, text='Browse', command=self.file_dialog2).grid(row=5, column=2, sticky='W')

        self.right_labels = ["Your email", "Your email password", "Your phone number", "Your Twilio phone number",
                             "Your Twilio account ID", "Your Twilio Auth token"]
        self.right_entry_labels = ['email', 'email_pwd_secret', 'your_phone', 'twilio_phone', 'account_sid_secret', 'auth_token_secret']
        self.right_entries = self.labels_entries(right_frame, self.right_labels, self.right_entry_labels)

        self.retrieve_values()

        self.message_frame = ttk.Label(big_frame, text="")
        self.message_frame.grid(row=1, columnspan=2)
        button_frame = ttk.Frame(big_frame)
        button_frame.grid(row=2, columnspan=2)
        ttk.Button(button_frame, text='Quit', command=root.quit).pack(side=LEFT)
        ttk.Button(button_frame, text='Update', command=self.get_values).pack(side=LEFT)


    def labels_entries(self, frame, labels, entry_labels):
        entries = {}
        for index, label in enumerate(labels):
            if entry_labels[index] != 'unencrypted_message':
                ttk.Label(frame, text=label).grid(row=index, sticky='E')
                if 'secret' in entry_labels[index]:
                    entries[entry_labels[index]] = ttk.Entry(frame, width=35, show='*')
                else:
                    entries[entry_labels[index]] = ttk.Entry(frame, width=35)
            else:
                ttk.Label(frame, text=label).grid(row=index, sticky='NE')
                entries[entry_labels[index]] = Text(frame, height=10, width=40, borderwidth=1, relief=SUNKEN)
            entries[entry_labels[index]].grid(row=index, column=1, sticky='W')

        return entries

    def file_dialog1(self):
        filename = filedialog.askopenfilename(initialdir='', title="Select a file")
        if filename != '':
            self.left_entries['file_to_encrypt'].delete(0, END)
        self.left_entries['file_to_encrypt'].insert(0, filename)


    def file_dialog2(self):
        filename = filedialog.askopenfilename(initialdir='', title="Select a file")
        if filename != '':
            self.left_entries['pubkey_file'].delete(0, END)
        self.left_entries['pubkey_file'].insert(0, filename)


    def get_values(self):
        for key, value in self.left_entries.items():
            if key == 'unencrypted_message':
                self.entry_values[key] = value.get(1.0, END)
            else:
                self.entry_values[key] = value.get()

        with open('./files/parameters.json', 'w') as params:
            params.write(json.dumps(self.entry_values, ensure_ascii=False))

        with open('./files/auth.json', 'w') as auth:
            auth_dict = {key: value.get() for key, value in self.right_entries.items()}
            auth.write(json.dumps(auth_dict))

        gpg = file_encryption.import_pubkey(self.entry_values['pubkey_file'])

        if gpg is not None:
            encrypted_file = file_encryption.encrypt_info(gpg, self.entry_values['file_to_encrypt'])
            self.message_frame.configure(text=f"File encrypted successfully: {Path(encrypted_file).name}")


    def retrieve_values(self):
        if Path('./files/parameters.json').exists():
            try:
                with open('./files/parameters.json', 'r') as params:
                    entry_values = json.loads(params.read())
                for key, value in entry_values.items():
                    if key != 'unencrypted_message':
                        self.left_entries[key].insert(0, value)
                    else:
                        self.left_entries[key].insert(1.0, value)
            except Exception as e:
                print(e)

        if Path('./files/auth.json').exists():
            try:
                with open('./files/auth.json', 'r') as auth:
                    auth_dict = json.loads(auth.read())

                for key in self.right_entry_labels:
                    try:
                        self.right_entries[key].insert(0, auth_dict[key])
                    except Exception as e:
                        self.right_entries[key].insert(0, "")
            except Exception as e:
                print(e)


if __name__ == '__main__':
    root = Tk()
    root.geometry("+300+300")
    app=App(root)

    if not Path('./files/').exists():
        Path('./files').mkdir()
    with open('./files/check_in.json', 'w') as check_in:
        check_in.write(json.dumps({'last_check_in': str(date.today())}))


    root.mainloop()
    #root.attributes('-topmost', True)
    #root.attributes('-topmost', False)

