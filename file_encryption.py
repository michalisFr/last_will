from pretty_bad_protocol import gnupg
from pathlib import Path
import shutil


def import_pubkey(pubkey):
    gpg = gnupg.GPG(homedir='./keys')

    try:
        if Path(pubkey).exists():
            try:
                with open(pubkey, 'rb') as key_file:
                    data = key_file.read()
                    gpg.import_keys(data)
            except Exception as e:
                print(f'Can\'t read the public key from file: {e}')
                return

        elif not Path(pubkey).is_file():
            print('This doesn\'t appear to be a valid public key filepath')
            return
        else:
            print('An unknown error occured')
            return

    except OSError:
        try:
            gpg.import_keys(pubkey)
        except Exception as e:
            print(f'This doesn\'t seem to be a valid public key: {e}')
            return

    return gpg


def encrypt_info(gpg, info_file):

    if Path(info_file).exists() and Path(info_file).is_file():
        key_id = gpg.list_keys()[0]['keyid']

        name = Path(info_file).name
        suffix = Path(info_file).suffix
        encrypted_path = Path('./files/')
        if not encrypted_path.exists():
            Path(encrypted_path).mkdir()

        encrypted_file = encrypted_path.joinpath(Path(f'{name}').with_suffix(suffix + '.gpg'))

        try:
            with open(info_file, 'rb') as message:
                try:
                    with open(encrypted_file, 'wb') as encrypted:
                        try:
                            gpg.encrypt(message, key_id, output=encrypted)
                        except:
                            print('The file couldn\'t be encrypted')
                            return
                except Exception as e:
                    print(f'The target file couldn\'t be opened: {e}')
                    return
        except:
            print('The source file couldn\'t be opened')
            return

        shutil.rmtree('./keys')
        return encrypted_file


if __name__ == '__main__':
    print("If you want to run this script standalone, edit it and provide the necessary parameters to the function calls")
    gpg = import_pubkey('') #Path to public key

    if gpg is not None:
        print(encrypt_info(gpg, '')) #Path to file to encrypt

    shutil.rmtree('./keys')