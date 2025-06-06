from vault.crypto import CryptoManager

class PasswordManager:
    def __init__(self, auth):
        key = auth._derive_key(getattr(auth, 'password', ''))
        self.crypto = CryptoManager(key)
        self.crypto.initialize_vault()

    def run(self):
        print("Bienvenue dans le gestionnaire de mots de passe.")
        # Ici on pourrait proposer un menu CLI : ajouter, lister, supprimer, etc.
