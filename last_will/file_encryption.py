from pretty_bad_protocol import gnupg
from pathlib import Path
import shutil


def import_pubkey(pubkey):
    """This function takes as argument the public key filepath, reads the key from file and adds it to the keychain.
    The key will be used in encrypt_info to encrypt the file.
    It returns a gpg object that contains all the info of the keychain (that has only that one public key)."""

    gpg = gnupg.GPG(homedir='./keys')

    try:
        if Path(pubkey).exists():
            try:
                with open(pubkey, 'rb') as key_file:
                    data = key_file.read()
                    gpg.import_keys(data)
            except OSError as e:
                return f"Can't open the public key file: {e}"

        elif not Path(pubkey).is_file():
            return "The path to the public key file doesn't appear to be valid"
        else:
            return "An unknown error occurred, while trying to read the public key from file."

    # This is a design decision that hasn't been implemented, where you can give the public key as text instead of file.
    # This exception would be raised if pubkey was not a path but instead a long string,
    # in which case Path(pubkey).exists raises an OSError.
    except OSError:
        try:
            gpg.import_keys(pubkey)
        except Exception as e:
            return f"This doesn't seem to be a valid public key: {e}"

    return gpg


def encrypt_info(gpg, info_file):
    """This function takes as arguments the gpg keychain and the filepath to the file to be encrypted
    It saves the file to disk and returns its path, which is ./file/<filename_as_it_was>.gpg"""

    if Path(info_file).exists() and Path(info_file).is_file():
        key_id = gpg.list_keys()[0]['keyid']  # The keychain contains only one key (index=0), read the keyid of that key.

        name = Path(info_file).name
        suffix = Path(info_file).suffix
        encrypted_path = Path('files/')
        if not encrypted_path.exists():
            Path(encrypted_path).mkdir()

        # Append the suffix .gpg to the file's filename. That way the filename of the original file is kept.
        encrypted_file = encrypted_path.joinpath(Path(f'{name}').with_suffix(suffix + '.gpg'))

        try:
            with open(info_file, 'rb') as message:
                try:
                    with open(encrypted_file, 'wb') as encrypted:
                        try:
                            gpg.encrypt(message, key_id, output=encrypted)
                            # Remove the public key from hard disk
                            shutil.rmtree('./keys')
                        except Exception as e:
                            shutil.rmtree('./keys')
                            return f"Fatal error. The file couldn't be encrypted. Error: {e}"
                except OSError as e:
                    shutil.rmtree('./keys')
                    return f"Fatal error. The target file couldn't be opened. Error: {e}"
        except OSError as e:
            shutil.rmtree('./keys')
            return f"Fatal error. The source file couldn't be opened. Error: {e}"

        return encrypted_file  # This is a Path object

    else:
        # Remove the public key from hard disk
        shutil.rmtree('./keys')

        return f"Fatal error. The source file couldn't be found."


if __name__ == '__main__':
    print(
        "If you want to run this script standalone, edit it and provide the necessary parameters to the function calls")
    gpg = import_pubkey('')  # Path to public key

    if gpg is not None:
        print(encrypt_info(gpg, ''))  # Path to file to encrypt

    # Remove the public key from hard disk
    shutil.rmtree('./keys')
