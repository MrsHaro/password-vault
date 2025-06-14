from cryptography.fernet import Fernet
import os
import json

class CryptoManager:
    def __init__(self, key: bytes, username: str):
        self.fernet = Fernet(key)
        vault_dir = os.path.join('data', 'vaults')
        if not os.path.exists(vault_dir):
            os.makedirs(vault_dir)
        self.vault_file = os.path.join(vault_dir, f'{username}.vault')

    def initialize_vault(self):
        if not os.path.exists(self.vault_file):
            token = self.fernet.encrypt(b'{}')
            with open(self.vault_file, 'wb') as f:
                f.write(token)

    def load_data(self) -> dict:
        with open(self.vault_file, 'rb') as f:
            token = f.read()
        data_json = self.fernet.decrypt(token)
        return json.loads(data_json)

    def save_data(self, data: dict):
        data_json = json.dumps(data).encode()
        token = self.fernet.encrypt(data_json)
        with open(self.vault_file, 'wb') as f:
            f.write(token)