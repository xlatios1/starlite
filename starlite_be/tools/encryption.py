import os
import hashlib
import base64
from cryptography.fernet import Fernet, InvalidToken

class Encryption():
    def __init__(self):
        self._cur_path = os.path.dirname(__file__)
        self._encrypted_path = os.path.join(self._cur_path, "__pycache__\.encrypted_data.txt")
        self._key = None
        
    # Function to set key
    def set_key(self, key):
        self._key = base64.urlsafe_b64encode(hashlib.sha256(key.encode()).digest())
        return True
        
    def check_if_exists(self):
        return os.path.exists(self._encrypted_path)

    def remove_saved_datas(self):
        if self.check_if_exists():
            try:
                os.remove(self._encrypted_path)
                print(f"encryption file removed successfully.")
            except:
                print("Error faced on removing encryption file. Do check if it is removed.")
                return False
        return True
    
    # Function to encrypt data and save it
    def encrypt_and_save_data(self, data):
        if self._key == None: return False
        fernet = Fernet(self._key)
        encrypted_data = fernet.encrypt(data.encode())
        with open(self._encrypted_path, "wb") as file:
            file.write(encrypted_data)
        return True

    # Function to decrypt data
    def decrypt_data(self):
        if self._key == None: return False
        fernet = Fernet(self._key)
        
        try: 
            with open(self._encrypted_path, "rb") as file:
                encrypted_data = file.read()
            return fernet.decrypt(encrypted_data).decode()
        except InvalidToken as e:
            print(f"Invalid token: {e}")
        except Exception as e:
            print(e)
        return False