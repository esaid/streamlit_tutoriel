import os
from deta import Deta
from dotenv import load_dotenv
import pickle
import streamlit_authenticator as stauth

# initialisation database DETA_KEY
load_dotenv(".env")  # la DETA_KEY est cache
DETA_KEY = os.getenv("DETA_KEY")
deta = Deta(DETA_KEY)
drive = deta.Drive("simple_drive")


# generation hashed_passwords et sauvegrde dans le fichier hashed_pwd.plk
def generate_hashed_passwords(name, username, password_):
    hashed_passwords = stauth.Hasher(password_).generate()

    # print(f"generation password :{hashed_passwords}")
    # ecriture du fichier passwords
    # print("ecriture fichier :")
    with open('hashed_pwd.plk', 'wb') as f:
        pickle.dump(name, f)
        pickle.dump(username, f)
        pickle.dump(hashed_passwords, f)
        f.close()


def read_hashed_passwords(file_):
    # lecture fichier hashed_pwd.plk
    with open(file_, 'rb') as f:
        name_ = pickle.load(f)
        username_ = pickle.load(f)
        password_ = pickle.load(f)
        f.close()
        return name_, username_, password_


def get_file_drive(name_drive, file_):
    d = deta.Drive(name_drive)
    get_d = d.get(f"{file_}")
    content = get_d.read()
    get_d.close()
    return content


def put_file_drive(name_drive, file_, path_local):
    d = deta.Drive(name_drive)
    d.put(f"{file_}", path=f"{path_local}/{file_}")


def delete_file_drive(name_drive, file_):
    d = deta.Drive(name_drive)
    d.delete(f"{file_}")


def list_files(name_drive):
    d = deta.Drive(name_drive)
    return d.list().get('names')

