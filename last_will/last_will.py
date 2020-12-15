from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from pathlib import Path
import json
from datetime import date


class App:
    def __init__(self, root):
        """This class creates the layout of the GUI with all the entry fields and labels.
        It also stores the values in two json files: parameters.json and auth.json.
        parameters.json contains all the parameters in the left column that concern the email with the private info
        auth.json contains all the parameters necessary to send emails and SMS (including credentials)
        If the details have already been filled previously, it populates the entry fields with them
        Finally, it calls the file_encryption functions to encrypt the file and save it to disk"""

        root.title('Last Will')

        # Create one big frame for the two smaller frames that are arranged in two columns
        big_frame = ttk.Frame(root)
        big_frame.pack()

        left_frame = ttk.Frame(big_frame)
        right_frame = ttk.Frame(big_frame)
        left_frame.grid(row=0, column=0, sticky=N)
        right_frame.grid(row=0, column=1, sticky=N)

        # Two lists with the labels and the entries' keys for the left entry fields
        self.left_labels = ["Name to appear as sender", "Recipient's email", "Email subject", "Unencrypted message",
                            "File to encrypt", "Recipient's PUBLIC Key"]
        self.left_entry_labels = ['sender_name', 'recipient_email', 'subject', 'unencrypted_message',
                                  'file_to_encrypt', 'pubkey_file']

        # Calls labels_entries that creates the labels and entries for the left column
        self.left_entries = self.labels_entries(left_frame, self.left_labels, self.left_entry_labels)
        self.entry_values = {}

        # Creates two buttons that call the respective functions that bring up a browse window
        ttk.Button(left_frame, text='Browse', command=self.file_to_encrypt_dialog).grid(row=4, column=2, sticky='W')
        ttk.Button(left_frame, text='Browse', command=self.pubkey_dialog).grid(row=5, column=2, sticky='W')

        # Two lists with the labels and the entries' keys for the right entry fields
        self.right_labels = ["Email to send from", "Email's password", "Your email", "Your phone number",
                             "Your Twilio phone number",
                             "Your Twilio account ID", "Your Twilio Auth token"]
        self.right_entry_labels = ['email', 'email_pwd_secret', 'your_email', 'your_phone', 'twilio_phone',
                                   'account_sid_secret', 'auth_token_secret']

        # Again calls labels_entries that creates the labels and entries for the right column
        self.right_entries = self.labels_entries(right_frame, self.right_labels, self.right_entry_labels)

        # Retrieve the values if they exist already and fills out the entry fields
        self.retrieve_values()

        # This creates an empty Label frame where messages will be displayed
        self.message_frame = ttk.Label(big_frame, text="")
        self.message_frame.grid(row=1, columnspan=2)

        # This creates a frame at the bottom for the buttons and the buttons Quit and Update
        button_frame = ttk.Frame(big_frame)
        button_frame.grid(row=2, columnspan=2)

        ttk.Button(button_frame, text='Quit', command=root.quit).pack(side=LEFT)  # Quits the app
        # Updates parameters.json and auth.json with the values in the entry fields. Also, encrypts the file.
        ttk.Button(button_frame, text='Update', command=self.update).pack(side=LEFT)

    def labels_entries(self, frame, labels, entry_labels):
        """This method creates the labels and entry fields for the GUI based on the lists provided as arguments"""

        entries = {}
        for index, label in enumerate(labels):
            # The Text frame requires different initialization than the Entry frames
            if entry_labels[index] != 'unencrypted_message':
                ttk.Label(frame, text=label).grid(row=index, sticky='E')

                # If the key contains the word 'secret' it means it's a credential, so show asterisks in the field
                if 'secret' in entry_labels[index]:
                    entries[entry_labels[index]] = ttk.Entry(frame, width=35, show='*')
                else:
                    entries[entry_labels[index]] = ttk.Entry(frame, width=35)
            else:
                ttk.Label(frame, text=label).grid(row=index, sticky='NE')
                entries[entry_labels[index]] = Text(frame, height=10, width=40, borderwidth=1, relief=SUNKEN)

            entries[entry_labels[index]].grid(row=index, column=1, sticky='W')

        return entries

    def file_to_encrypt_dialog(self):
        """This method opens a browse window and receives the path of the file to be encrypted.
        Then it adds the path to the entry field"""

        filename = filedialog.askopenfilename(initialdir='', title="Select a file")

        # If the entry field isn't empty, delete the entry first and then replace it with the new filename
        if filename != '':
            self.left_entries['file_to_encrypt'].delete(0, END)
        self.left_entries['file_to_encrypt'].insert(0, filename)

    def pubkey_dialog(self):
        """This method opens a browse window and receives the path of the public key file.
        Then it adds the path to the entry field"""

        filename = filedialog.askopenfilename(initialdir='', title="Select a file")

        # If the entry field isn't empty, delete the entry first and then replace it with the new filename
        if filename != '':
            self.left_entries['pubkey_file'].delete(0, END)
        self.left_entries['pubkey_file'].insert(0, filename)

    def update(self):
        """This method is called when the Update button is clicked.
        It reads the entries from the entry fields and updates parameters.json and auth.json.
        Any empty fields are stored as "", which guarantees that the keys will exist.
        It also calls file_encryption functions to encrypt the file and then saves it"""

        # Get the values from the left entry fields
        for key, value in self.left_entries.items():
            if key == 'unencrypted_message':
                self.entry_values[key] = value.get(1.0, END)
            else:
                self.entry_values[key] = value.get()

        # Get the values from the parameters.json file.
        # We want to compare the filenames in the file with the ones in the fields, to check if they've changed.
        try:
            with open('files/parameters.json', 'r') as params:
                entry_values_in_file = json.loads(params.read())
        except OSError as e:
            self.message_frame.configure(text=f"Fatal error. Couldn't open parameters.json. Error: {e}")
        except TypeError as e:
            self.message_frame.configure(text=f"Couldn't write Parameter values as JSON. Error: {e}")

        # Call import_pubkey from file_enryption and get back the keychain
        gpg = file_encryption.import_pubkey(self.entry_values['pubkey_file'])

        # If the return value is a string, then an error occurred, which is displayed in self.message_frame
        # Also we'll keep the filenames already in parameters.json
        successfully_encrypted = False
        if type(gpg) is not str:
            # Call encrypt_info from file encryption and get back the path to the encrypted file (a Path object)
            encrypted_file = file_encryption.encrypt_info(gpg, self.entry_values['file_to_encrypt'])

            # If the return value is a string or None, then an error occurred, which is displayed in self.message_frame
            # Also we'll keep the filenames already in parameters.json
            if type(encrypted_file) is not str:
                self.message_frame.configure(text=f"File encrypted successfully: {Path(encrypted_file).name}")
                successfully_encrypted = True
            else:
                self.message_frame.configure(text=encrypted_file + "\nThe encrypted and pubkey files haven't changed.")
        else:
            self.message_frame.configure(text=gpg + "\nThe encrypted and pubkey files haven't changed.")

        # We keep the filenames already in parameters.json
        if not successfully_encrypted:
            self.entry_values['file_to_encrypt'] = entry_values_in_file['file_to_encrypt']
            self.entry_values['pubkey_file'] = entry_values_in_file['pubkey_file']

        # Delete any pre-existing .gpg files in the ./files folder
        existing_file = Path('files').joinpath(Path(self.entry_values['file_to_encrypt']).name + '.gpg')
        for file in Path('files').iterdir():
            if file.suffix == '.gpg' and file != existing_file:
                Path(file).unlink()

        # Write the values in parameters.json
        try:
            with open('files/parameters.json', 'w') as params:
                params.write(json.dumps(self.entry_values, ensure_ascii=False))
        except OSError as e:
            self.message_frame.configure(text=f"Fatal error. Couldn't open parameters.json. Error: {e}")
        except TypeError as e:
            self.message_frame.configure(text=f"Couldn't write Parameter values as JSON. Error: {e}")

        # Read the values of the right entry fields and write them to auth.json
        try:
            with open('files/auth.json', 'w') as auth:
                auth_dict = {key: value.get() for key, value in self.right_entries.items()}
                auth.write(json.dumps(auth_dict))
        except OSError as e:
            self.message_frame.configure(text=f"Couldn't open parameters.json. Error: {e}")
        except TypeError as e:
            self.message_frame.configure(text=f"Couldn't write Auth values as JSON. Error: {e}")

        print(self.message_frame.grab_current())

    def retrieve_values(self):
        """This method retrieves the values from the JSON files and populates the entry fields."""

        if Path('files/parameters.json').exists():
            try:
                with open('files/parameters.json', 'r') as params:
                    entry_values = json.loads(params.read())
                for key, value in entry_values.items():
                    if key != 'unencrypted_message':
                        self.left_entries[key].insert(0, value)
                    else:
                        self.left_entries[key].insert(1.0, value)
            except OSError as e:
                self.message_frame.configure(text=f"Couldn't open parameters.json to read the entries. "
                                                  f"If this the first time your run the app ignore this error. "
                                                  f"Error: {e}")

        if Path('files/auth.json').exists():
            try:
                with open('files/auth.json', 'r') as auth:
                    auth_dict = json.loads(auth.read())

                for key in self.right_entry_labels:
                    try:
                        self.right_entries[key].insert(0, auth_dict[key])
                    except Exception as e:
                        self.right_entries[key].insert(0, "")
            except OSError as e:
                self.message_frame.configure(text=f"Couldn't open auth.json to read the entries. "
                                                  f"If this the first time your run the app ignore this error. "
                                                  f"Error: {e}")


if __name__ == '__main__':
    root = Tk()  # Create the window
    root.geometry("+300+300")  # Place it in the middle of the screen
    app = App(root)

    if not Path('files/').exists():
        Path('files').mkdir()

    # When you open the app this is considered a check in and the current date is written to check_in.json
    # This means that if there's a deadline key in the file it's removed
    try:
        with open('files/check_in.json', 'w') as check_in:
            check_in.write(json.dumps({'last_check_in': str(date.today())}))
    except OSError as e:
        print(f"Fatal error. Couldn't open check_in.json to write the current date. Error: {e}")

    root.mainloop()
    # root.attributes('-topmost', True)
    # root.attributes('-topmost', False)
