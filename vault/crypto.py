from cryptography.fernet import Fernet
import os
import json

class CryptoManager:
    VAULT_FILE = os.path.join('data', 'vault.enc')

    def __init__(self, key: bytes):

        self.fernet = Fernet(key)

    def initialize_vault(self):

        if not os.path.exists(self.VAULT_FILE):
            token = self.fernet.encrypt(b'{}')
            with open(self.VAULT_FILE, 'wb') as f:
                f.write(token)

    def load_data(self) -> dict:
        with open(self.VAULT_FILE, 'rb') as f:
            token = f.read()
        data_json = self.fernet.decrypt(token)
        return json.loads(data_json)

    def save_data(self, data: dict):
        data_json = json.dumps(data).encode()
        token = self.fernet.encrypt(data_json)
        with open(self.VAULT_FILE, 'wb') as f:
            f.write(token)