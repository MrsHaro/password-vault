import os
import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import json

class Authenticator:
    SALT_FILE = os.path.join('data', 'salt.bin')
    HASH_FILE = os.path.join('data', 'master.hash')

    def __init__(self):
        self.salt = None
        self.backend = default_backend()
        if os.path.exists(self.SALT_FILE):
            with open(self.SALT_FILE, 'rb') as f:
                self.salt = f.read()

    def is_initialized(self) -> bool:
        return os.path.exists(self.HASH_FILE) and self.salt is not None

    def setup_master_password(self):
        while True:
            pwd = getpass.getpass('Définissez un mot de passe maître : ')
            pwd_confirm = getpass.getpass('Confirmez le mot de passe maître : ')
            if pwd != pwd_confirm:
                print('Les mots de passe ne correspondent pas, réessayez.')
            else:
                break
        self.salt = os.urandom(16) 
        with open(self.SALT_FILE, 'wb') as f:
            f.write(self.salt)
        key = self._derive_key(pwd)
        with open(self.HASH_FILE, 'wb') as f:
            f.write(key)
        print('Mot de passe maître configuré avec succès.')

    def verify_master_password(self) -> bool:
      pwd = getpass.getpass('Entrez le mot de passe maître : ')
      key_try = self._derive_key(pwd)
      with open(self.HASH_FILE, 'rb') as f:
        key_true = f.read()
      if key_try == key_true:
        self.password = pwd
        return True
      return False

    def _derive_key(self, password: str) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100_000,
            backend=self.backend
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))